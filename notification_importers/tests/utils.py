from django.core.exceptions import ObjectDoesNotExist


def serialize_notifications(notifications):
    return "\n".join([serialize_notification(n) for n in notifications])


def serialize_notification(notification):
    values = [notification.type]
    for field in ("subject", "body_text", "body_html"):
        for language in ("fi", "en", "sv"):
            try:
                translation = notification.translations.get(language_code=language)
                value = getattr(translation, field)
            except ObjectDoesNotExist:
                value = ""
            values.append(value)
    return "|".join(values)
