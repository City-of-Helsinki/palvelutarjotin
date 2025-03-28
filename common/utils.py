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
        f"User does not have permission to edit this {expected_obj_type.__name__}"
    )


def raise_permission_denied_if_not_staff(user):
    """
    Raise PermissionDenied if user is not staff
    :raises django.core.exceptions.PermissionDenied: If user is not staff
    """
    if not user or not getattr(user, "is_staff"):
        raise PermissionDenied(_("You do not have permission to perform this action"))


def get_client_ip(request: Optional[HttpRequest]) -> Optional[str]:
    """
    Retrieves the client's IP address from the request.

    This function prioritizes the 'HTTP_X_FORWARDED_FOR' header, which is commonly
    used when the request passes through proxies or load balancers. If that
    header is not available, it falls back to 'REMOTE_ADDR'.

    Args:
        request: The HttpRequest object, or None if no request is available.

    Returns:
        The client's IP address as a string, or None if it cannot be determined or
        if request is None.
    """
    if not request:
        return None

    try:
        x_forwarded_for: Optional[str] = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ips = x_forwarded_for.split(",")
            if ips:  # check if list is not empty
                return ips[0].strip()

        remote_addr: Optional[str] = request.META.get("REMOTE_ADDR")
        if remote_addr:
            return remote_addr

        return None

    except (AttributeError, IndexError):
        return None  # Handle potential errors gracefully
    except Exception as e:  # Catch any other error.
        print(f"An unexpected error occured: {e}")
        return None
