import graphene
from django_ilmoitin.api.schema import (
    NotificationTemplateNode as IlmotinNotificationTemplateNode,
)
from django_ilmoitin.models import NotificationTemplate, NotificationTemplateException
from django_ilmoitin.registry import notifications
from django_ilmoitin.utils import render_notification_template
from graphene import Field, JSONString, ObjectType

import graphene_linked_events.schema
import occurrences.schema
import organisations.schema
import servicemap.schema
from common.utils import LanguageEnum, map_enums_to_values_in_kwargs
from palvelutarjotin.exceptions import ApiUsageError


class NotificationTemplateWithContext(ObjectType):
    template = graphene.Field(IlmotinNotificationTemplateNode)
    custom_context_preview_html = graphene.String()
    custom_context_preview_text = graphene.String()


class Mutation(
    graphene_linked_events.schema.Mutation,
    organisations.schema.Mutation,
    occurrences.schema.Mutation,
    graphene.ObjectType,
):
    pass


NotificationTemplateTypeEnum = graphene.Enum(
    "NotificationTemplateType",
    [(lang[0].upper(), lang[0]) for lang in notifications.registry.items()],
)


class Query(
    graphene_linked_events.schema.Query,
    servicemap.schema.Query,
    organisations.schema.Query,
    occurrences.schema.Query,
    graphene.ObjectType,
):
    notification_template = Field(
        NotificationTemplateWithContext,
        template_type=NotificationTemplateTypeEnum(),
        context=JSONString(
            required=True,
            description="Json stringify value of context variables used in the "
            "template",
        ),
        language=LanguageEnum(required=True),
    )

    @staticmethod
    @map_enums_to_values_in_kwargs
    def resolve_notification_template(parent, info, **kwargs):
        try:
            template = NotificationTemplate.objects.get(type=kwargs["template_type"])
        except NotificationTemplate.DoesNotExist:
            return None

        context = kwargs["context"]

        # Preview mode meaning only template inside the
        # {% if preview_mode %} ... {% endif %} will be rendered
        # This to bypass complex object expression used in actual email template which
        # is most likely not available in the context sending from client

        context["preview_mode"] = True
        language = kwargs["language"]
        try:
            custom_context_preview = render_notification_template(
                template, context, language
            )
        except NotificationTemplateException:
            raise ApiUsageError(
                "Missing template translation or incorrect context variable"
            )
        return NotificationTemplateWithContext(
            template=template,
            custom_context_preview_html=custom_context_preview.body_html,
            custom_context_preview_text=custom_context_preview.body_text,
        )


schema = graphene.Schema(query=Query, mutation=Mutation)
