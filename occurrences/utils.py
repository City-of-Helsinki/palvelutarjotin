from django_ilmoitin.utils import send_notification


def send_event_notifications_to_contact_person(
    occurrence, study_group, notification_type, **kwargs
):
    context = {
        "occurrence": occurrence,
        "study_group": study_group,
        **kwargs,
    }
    # TODO: Send notification based on user language
    send_notification(
        study_group.person.email_address, notification_type, context=context,
    )
