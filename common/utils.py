from django.db import transaction
from graphql_relay import from_global_id

from palvelutarjotin import __version__
from palvelutarjotin.exceptions import DataValidationError, IncorrectGlobalIdError
from palvelutarjotin.settings import REVISION


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
