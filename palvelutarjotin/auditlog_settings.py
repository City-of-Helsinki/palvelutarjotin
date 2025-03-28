# Register all models by default
AUDITLOG_INCLUDE_ALL_MODELS = True

# Exclude the IP address from logging?
# When using AuditlogMiddleware, the IP address is logged by default
AUDITLOG_DISABLE_REMOTE_ADDR = False

# Disables logging during raw save. (I.e. for instance using loaddata)
# M2M operations will still be logged, since they’re never considered raw.
AUDITLOG_DISABLE_ON_RAW_SAVE = True

# Exclude models in registration process.
# This setting will only be considered when AUDITLOG_INCLUDE_ALL_MODELS is True.
AUDITLOG_EXCLUDE_TRACKING_MODELS = (
    "admin.logentry",  # excluded by default
    "auditlog.logentry",  # excluded by default
    "contenttypes.contenttype",  # system model
    "sessions.session",  # auth model
    "helusers.oidcbackchannellogoutevent",  # auth model
    "mailer.dontsendentry",  # system
    "mailer.message",  # system
    "mailer.messagelog",  # system
    # social-auth-app-django models
    # https://github.com/python-social-auth/social-app-django/blob/master/social_django/models.py
    "social_django.association",  # auth model
    "social_django.code",  # auth model
    "social_django.nonce",  # auth model
    "social_django.partial",  # auth model
    "social_django.usersocialauth",  # auth model
    "axes.accesslog",  # system model
    "axes.accessattempt",  # system model
    "axes.accessfailurelog",  # system model
    "django_ilmoitin.notificationtemplate_admins_to_notify",  # system model
    "django_ilmoitin.notificationtemplatetranslation",  # system model
    "occurrences.language",  # unimportant and causes lots of issues with factory
    "verification_token.verificationtoken",  # system model
)

# Configure models registration and other behaviours.
AUDITLOG_INCLUDE_TRACKING_MODELS = (
    "organisations.User",
    "organisations.Organisation",
    "auth.group_permissions",
    "django_ilmoitin.notificationtemplate",
    "auth.permission",
    "helusers.adgroup",
    "occurrences.occurrence",
    "helusers.adgroupmapping",
    "organisations.user_user_permissions",
    "occurrences.studyleveltranslation",
    "occurrences.eventqueueenrolment",
    "organisations.organisation_persons",
    "occurrences.enrolleepersonaldata",
    "occurrences.occurrence_languages",
    "occurrences.studygroup",
    "occurrences.studygroup_study_levels",
    "occurrences.venuecustomdatatranslation",
    "reports.enrolmentreport",
    "occurrences.studylevel",
    "auth.group",
    "occurrences.enrolment",
    "organisations.user_groups",
    "occurrences.palvelutarjotinevent",
    "occurrences.venuecustomdata",
    "occurrences.occurrence_contact_persons",
    "organisations.user_ad_groups",
    "organisations.person",
    "occurrences.palvelutarjotineventtranslation",
    "organisations.organisationproposal",
)
