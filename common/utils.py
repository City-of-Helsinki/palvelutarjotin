from datetime import datetime

import graphene
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone
from graphene import Node
from graphql_relay import from_global_id

from palvelutarjotin import __version__
from palvelutarjotin.exceptions import (
    DataValidationError,
    IncorrectGlobalIdError,
    ObjectDoesNotExistError,
)
from palvelutarjotin.settings import REVISION

LanguageEnum = graphene.Enum(
    "Language", [(l[0].upper(), l[0]) for l in settings.LANGUAGES]
)

LINKED_EVENT_DATE_FORMAT = "%Y-%m-%d"


def format_linked_event_date(datetime_obj):
    return datetime_obj.strftime(LINKED_EVENT_DATE_FORMAT)


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
    if translations_input:
        model.create_or_update_translations(translations_input)
    update_object(model, model_data)


def get_api_version():
    return " | ".join((__version__, REVISION.decode("utf-8")))


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


def get_obj_from_global_id(info, global_id, expected_obj_type):
    obj = Node.get_node_from_global_id(info, global_id)
    if not obj or type(obj) != expected_obj_type:
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
