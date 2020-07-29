from django.utils.translation import ugettext_lazy as _

NOTIFICATION_TYPE_EMAIL = "email"
NOTIFICATION_TYPE_SMS = "sms"
NOTIFICATION_TYPE_ALL = "email_sms"
NOTIFICATION_TYPES = (
    (NOTIFICATION_TYPE_ALL, _("email and sms")),
    (NOTIFICATION_TYPE_EMAIL, _("email")),
    (NOTIFICATION_TYPE_SMS, _("sms")),
)


class NotificationTemplate:
    OCCURRENCE_ENROLMENT = "occurrence_enrolment"
    OCCURRENCE_UNENROLMENT = "occurrence_unenrolment"
    ENROLMENT_APPROVED = "enrolment_approved"
    ENROLMENT_DECLINED = "enrolment_declined"

    OCCURRENCE_ENROLMENT_SMS = "occurrence_enrolment_sms"
    OCCURRENCE_UNENROLMENT_SMS = "occurrence_unenrolment_sms"
    ENROLMENT_APPROVED_SMS = "enrolment_approved_sms"
    ENROLMENT_DECLINED_SMS = "enrolment_declined_sms"
