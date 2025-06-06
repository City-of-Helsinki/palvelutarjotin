import enum
from datetime import datetime
from typing import Optional

import graphene
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from graphene import Node
from graphql_relay import from_global_id

from palvelutarjotin import __version__
from palvelutarjotin.exceptions import (
    DataValidationError,
    IncorrectGlobalIdError,
    ObjectDoesNotExistError,
)

LINKED_EVENT_DATE_FORMAT = "%Y-%m-%d"

LanguageEnum = graphene.Enum(
    "Language", [(lang[0].upper(), lang[0]) for lang in settings.LANGUAGES]
)


def is_enum_value(value):
    """
    Check if a value is an enum value, e.g. TestEnum.FI
    where TestEnum derives from enum.Enum or graphene.Enum.
    """
    # Works both for enum.Enum and graphene.Enum
    return type(type(value)) is enum.EnumMeta


def deepfix_enum_values(data):
    """
    Fix enum values recursively in/out of dictionaries, lists, sets, and tuples.
    """
    if isinstance(data, dict):
        return {deepfix_enum_values(k): deepfix_enum_values(v) for k, v in data.items()}
    elif isinstance(data, (list, set, tuple)):
        return type(data)(deepfix_enum_values(v) for v in data)
    elif is_enum_value(data):
        return data.value
    else:
        return data


def map_enums_to_values_in_kwargs(method):
    """
    Decorator that maps enums to their values in keyword arguments.
    """

    def wrapper(*args, **kwargs):
        fixed_kwargs = deepfix_enum_values(kwargs)
        return method(*args, **fixed_kwargs)

    return wrapper


def format_linked_event_datetime(datetime_obj):
    if not datetime_obj:
        return None
    return datetime_obj.isoformat(timespec="seconds")


def update_object(obj, data):
    if not data:
        return
    for k, v in data.items():
        if v is None and not obj.__class__._meta.get_field(k).null:
            raise DataValidationError(f"{k} cannot be null.")
        setattr(obj, k, v)
    obj.save()


@transaction.atomic
def update_object_with_translations(model, model_data):
    translations_input = model_data.pop("translations", None)
    if translations_input is not None:
        model.create_or_update_translations(translations_input)
    update_object(model, model_data)


def get_api_version():
    return " | ".join((__version__, settings.COMMIT_HASH.decode("utf-8")))


def get_node_id_from_global_id(global_id, node_name):
    name, id = from_global_id(global_id)
    if name != node_name:
        raise IncorrectGlobalIdError("Node type does not match")
    return id


def convert_to_localtime_tz(value):
    dt = datetime.combine(datetime.now().date(), value)
    if timezone.is_naive(value):
        # Auto add local timezone to naive time
        return timezone.make_aware(dt).timetz()
    else:
        return timezone.localtime(dt).timetz()


def to_local_datetime_if_naive(value) -> datetime:
    """
    Convert ISO 8601 formatted string to datetime object and
    convert it to local timezone if no timezone information was specified
    (i.e. the converted datetime was a naive datetime).
    Otherwise, return the converted datetime object as is.

    :param value: ISO 8601 formatted string
    :return: datetime object
    :raises ValueError: If the input string is not a valid ISO 8601 formatted string
    :raises TypeError: If the input string is not a string
    """
    result = datetime.fromisoformat(value)
    if timezone.is_naive(result):
        return timezone.make_aware(result)
    return result


def get_obj_from_global_id(info, global_id, expected_obj_type):
    obj = Node.get_node_from_global_id(info, global_id)
    if not obj or type(obj) is not expected_obj_type:
        raise ObjectDoesNotExistError(
            f"{expected_obj_type.__name__} matching query does not exist."
        )
    return obj


def get_editable_obj_from_global_id(info, global_id, expected_obj_type):
    obj = get_obj_from_global_id(info, global_id, expected_obj_type)
    try:
        if obj.is_editable_by_user(info.context.user):
            return obj
    except AttributeError:
        raise TypeError(
            f"{obj.__class__.__name__} model does not implement is_editable_by_user()."
        )
    raise PermissionDenied(
        f"User does not have permission to edit this {expected_obj_type.__name__}."
    )


def raise_permission_denied_if_not_event_staff(user):
    """
    Raise PermissionDenied if user is not event staff
    :raises django.core.exceptions.PermissionDenied: If user is not event staff
    """
    if not user or not getattr(user, "is_event_staff", False):
        raise PermissionDenied(
            _("User does not have permission to perform this admin action.")
        )


def get_client_ip(request: Optional[HttpRequest]) -> Optional[str]:
    """
    Retrieves the client's IP address from the request, removing any port.

    Prioritizes 'HTTP_X_FORWARDED_FOR' and then falls back to 'REMOTE_ADDR'.
    Removes any trailing port number.
    """
    if not request:
        return None

    ip_address = request.headers.get("X-Forwarded-For")
    if ip_address:
        client_ip = ip_address.split(",")[0].strip()
        if ":" in client_ip:
            return client_ip.split(":")[0]
        return client_ip

    ip_address = request.META.get("REMOTE_ADDR")
    if ip_address:
        if ":" in ip_address:
            if "[" in ip_address and "]" in ip_address:
                # IPv6 with brackets: [address]:port
                return ip_address.split("]")[0][1:]
            elif "." in ip_address:
                # IPv4: address:port
                return ip_address.split(":")[0]
            else:
                # Likely IPv6 without brackets: address:port
                parts = ip_address.split(":")
                if len(parts) > 1 and parts[-1].isdigit():
                    return ":".join(parts[:-1])
                else:
                    return ip_address
        return ip_address

    return None
