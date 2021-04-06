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
    OCCURRENCE_CANCELLED = "occurrence_cancelled"
    ENROLMENT_APPROVED = "enrolment_approved"
    ENROLMENT_DECLINED = "enrolment_declined"
    ENROLMENT_CANCELLATION = "enrolment_cancellation"
    ENROLMENT_CANCELLED = "enrolment_cancelled"
    ENROLMENT_SUMMARY_REPORT = "enrolment_summary_report"

    OCCURRENCE_ENROLMENT_SMS = "occurrence_enrolment_sms"
    OCCURRENCE_UNENROLMENT_SMS = "occurrence_unenrolment_sms"
    ENROLMENT_APPROVED_SMS = "enrolment_approved_sms"
    ENROLMENT_DECLINED_SMS = "enrolment_declined_sms"
    ENROLMENT_CANCELLATION_SMS = "enrolment_cancellation_sms"
    ENROLMENT_CANCELLED_SMS = "enrolment_cancelled_sms"
    OCCURRENCE_CANCELLED_SMS = "occurrence_cancelled_sms"


class StudyGroupStudyLevels:
    """
    2021-01-14: Study levels were migrated from
    StudyGroup model's CharField to a new StudyLevel
    model / tabel in task PT-686.
    """

    STUDY_LEVEL_PRESCHOOL = "preschool"
    STUDY_LEVEL_AGE_0_2 = "age_0_2"
    STUDY_LEVEL_AGE_3_4 = "age_3_4"
    STUDY_LEVEL_GRADE_1 = "grade_1"
    STUDY_LEVEL_GRADE_2 = "grade_2"
    STUDY_LEVEL_GRADE_3 = "grade_3"
    STUDY_LEVEL_GRADE_4 = "grade_4"
    STUDY_LEVEL_GRADE_5 = "grade_5"
    STUDY_LEVEL_GRADE_6 = "grade_6"
    STUDY_LEVEL_GRADE_7 = "grade_7"
    STUDY_LEVEL_GRADE_8 = "grade_8"
    STUDY_LEVEL_GRADE_9 = "grade_9"
    STUDY_LEVEL_GRADE_10 = "grade_10"
    STUDY_LEVEL_SECONDARY = "secondary"
    STUDY_LEVEL_OTHER = "other"

    # The order of this STUDY_LEVELS will be the order returned in GraphQL API
    STUDY_LEVELS = (
        (STUDY_LEVEL_AGE_0_2, _("age 0-2")),
        (STUDY_LEVEL_AGE_3_4, _("age 3-4")),
        (STUDY_LEVEL_PRESCHOOL, _("preschool")),
        (STUDY_LEVEL_GRADE_1, _("first grade")),
        (STUDY_LEVEL_GRADE_2, _("second grade")),
        (STUDY_LEVEL_GRADE_3, _("third grade")),
        (STUDY_LEVEL_GRADE_4, _("fourth grade")),
        (STUDY_LEVEL_GRADE_5, _("fifth grade")),
        (STUDY_LEVEL_GRADE_6, _("sixth grade")),
        (STUDY_LEVEL_GRADE_7, _("seventh grade")),
        (STUDY_LEVEL_GRADE_8, _("eighth grade")),
        (STUDY_LEVEL_GRADE_9, _("ninth grade")),
        (STUDY_LEVEL_GRADE_10, _("tenth grade")),
        (STUDY_LEVEL_SECONDARY, _("secondary")),
        (STUDY_LEVEL_OTHER, _("other group")),
    )
