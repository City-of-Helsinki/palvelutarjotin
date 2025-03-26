import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import environ
import sentry_sdk
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

from palvelutarjotin.consts import CSP

checkout_dir = environ.Path(__file__) - 2
assert os.path.exists(checkout_dir("manage.py"))

parent_dir = checkout_dir.path("..")
if os.path.isdir(parent_dir("etc")):
    env_file = parent_dir("etc/env")
    default_var_root = environ.Path(parent_dir("var"))
else:
    env_file = checkout_dir(".env")
    default_var_root = environ.Path(checkout_dir("var"))

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ""),
    MEDIA_ROOT=(environ.Path(), environ.Path(checkout_dir("var"))("media")),
    STATIC_ROOT=(environ.Path(), default_var_root("static")),
    MEDIA_URL=(str, "/media/"),
    STATIC_URL=(str, "/static/"),
    ENVIRONMENT_URL=(str, ""),
    ALLOWED_HOSTS=(list, []),
    USE_X_FORWARDED_HOST=(bool, False),
    DATABASE_URL=(str, ""),
    CACHE_URL=(str, "locmemcache://"),
    MAILER_EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
    MAILER_LOCK_PATH=(str, ""),
    DEFAULT_FROM_EMAIL=(str, "no-reply@hel.ninja"),
    DEFAULT_SMS_SENDER=(str, "Hel.fi"),
    ILMOITIN_TRANSLATED_FROM_EMAIL=(dict, {}),
    TRANSLATED_SMS_SENDER=(dict, {}),
    MAIL_MAILGUN_KEY=(str, ""),
    MAIL_MAILGUN_DOMAIN=(str, ""),
    MAIL_MAILGUN_API=(str, ""),
    SENTRY_DSN=(str, ""),
    SENTRY_ENVIRONMENT=(str, ""),
    CORS_ALLOWED_ORIGINS=(list, []),
    CORS_ALLOWED_ORIGIN_REGEXES=(list, []),
    CORS_ORIGIN_ALLOW_ALL=(bool, False),
    TOKEN_AUTH_ACCEPTED_SCOPE_PREFIX=(str, ""),
    TOKEN_AUTH_REQUIRE_SCOPE_PREFIX=(bool, False),
    TOKEN_AUTH_ACCEPTED_AUDIENCE=(list, ["kultus-api-dev"]),
    TOKEN_AUTH_AUTHSERVER_URL=(
        list,
        ["https://tunnistus.test.hel.ninja/auth/realms/helsinki-tunnistus/"],
    ),
    ILMOITIN_QUEUE_NOTIFICATIONS=(bool, False),
    ENABLE_GRAPHIQL=(bool, False),
    LINKED_EVENTS_API_ROOT=(str, "https://api.hel.fi/linkedevents/v1/"),
    LINKED_EVENTS_API_KEY=(str, ""),
    LINKED_EVENTS_DATA_SOURCE=(str, "palvelutarjotin"),
    SERVICEMAP_API_ROOT=(str, "https://www.hel.fi/palvelukarttaws/rest/v4/unit/"),
    NOTIFICATION_SERVICE_SMS_ENABLED=(bool, True),
    NOTIFICATION_SERVICE_API_TOKEN=(str, ""),
    NOTIFICATION_SERVICE_API_URL=(str, "https://notification-service.hel.fi/v1/"),
    CAPTCHA_ENABLED=(bool, False),
    RECAPTCHA_SECRET_KEY=(str, ""),
    KEYWORD_SET_CATEGORY_ID=(str, "kultus:categories"),
    KEYWORD_SET_TARGET_GROUP_ID=(str, "kultus:target_groups"),
    KEYWORD_SET_ADDITIONAL_CRITERIA_ID=(str, "kultus:additional_criteria"),
    KEYWORD_SET_ACTIVITIES_ID=(str, "kultus:additional_criteria"),
    KULTUS_PROVIDER_UI_BASE_URL=(str, "https://kultus-admin.hel.fi/"),
    KULTUS_TEACHER_UI_BASE_URL=(str, "https://kultus.hel.fi/"),
    ENABLE_SUMMARY_REPORT=(bool, False),
    VERIFICATION_TOKEN_VALID_MINUTES=(int, 15),
    PERSONAL_DATA_RETENTION_PERIOD_MONTHS=(int, 24),
    UPDATE_LAST_LOGIN_ENABLED=(bool, True),
    UPDATE_LAST_LOGIN_INTERVAL_MINUTES=(int, 60),
    APP_RELEASE=(str, ""),
    GDPR_API_QUERY_SCOPE=(str, "gdprquery"),
    GDPR_API_DELETE_SCOPE=(str, "gdprdelete"),
    TOKEN_AUTH_API_AUTHORIZATION_FIELD=(str, "authorization.permissions.scopes"),
    HELUSERS_BACK_CHANNEL_LOGOUT_ENABLED=(bool, False),
    HELUSERS_USER_MIGRATE_ENABLED=(bool, False),
)

if os.path.exists(env_file):
    env.read_env(env_file)

BASE_DIR = str(checkout_dir)

DEBUG = env.bool("DEBUG")
SECRET_KEY = env.str("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "The SECRET_KEY setting must not be empty. "
        "See README.md for instructions how to generate a new secret key."
    )

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
USE_X_FORWARDED_HOST = env.bool("USE_X_FORWARDED_HOST")

DATABASES = {"default": env.db()}

CACHES = {"default": env.cache()}

if env.str("DEFAULT_FROM_EMAIL"):
    DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")

if env.str("DEFAULT_SMS_SENDER"):
    DEFAULT_SMS_SENDER = env.str("DEFAULT_SMS_SENDER")

NOTIFICATION_SERVICE_SMS_ENABLED = env.bool("NOTIFICATION_SERVICE_SMS_ENABLED")
NOTIFICATION_SERVICE_API_TOKEN = env.str("NOTIFICATION_SERVICE_API_TOKEN")
NOTIFICATION_SERVICE_API_URL = env.str("NOTIFICATION_SERVICE_API_URL")

if env("MAIL_MAILGUN_KEY"):
    ANYMAIL = {
        "MAILGUN_API_KEY": env("MAIL_MAILGUN_KEY"),
        "MAILGUN_SENDER_DOMAIN": env("MAIL_MAILGUN_DOMAIN"),
        "MAILGUN_API_URL": env("MAIL_MAILGUN_API"),
    }
EMAIL_BACKEND = "mailer.backend.DbBackend"
MAILER_EMAIL_BACKEND = env.str("MAILER_EMAIL_BACKEND")

_tmp_mailer_dir = None
if env("MAILER_LOCK_PATH"):
    MAILER_LOCK_PATH = env.str("MAILER_LOCK_PATH")
else:
    # Create a temporary directory for mailer lock file.
    # Stored as a module-level variable to keep the TemporaryDirectory instance
    # alive for the entire process lifetime.
    #
    # From https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory
    # "This class securely creates a temporary directory" and
    # "On completion of the context or destruction of the temporary directory object,
    # the newly created temporary directory and all its contents are removed from
    # the filesystem."
    _tmp_mailer_dir = tempfile.TemporaryDirectory(prefix="kultus-mailer-")
    MAILER_LOCK_PATH = Path(_tmp_mailer_dir.name) / "mailer_lockfile"

ILMOITIN_TRANSLATED_FROM_EMAIL = env("ILMOITIN_TRANSLATED_FROM_EMAIL")
ILMOITIN_QUEUE_NOTIFICATIONS = env("ILMOITIN_QUEUE_NOTIFICATIONS")
TRANSLATED_SMS_SENDER = env("TRANSLATED_SMS_SENDER")

try:
    COMMIT_HASH = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
except Exception:
    COMMIT_HASH = b"n/a"

sentry_sdk.init(
    dsn=env.str("SENTRY_DSN"),
    release=COMMIT_HASH,
    environment=env("SENTRY_ENVIRONMENT"),
    integrations=[DjangoIntegration()],
)

MEDIA_ROOT = env("MEDIA_ROOT")
STATIC_ROOT = env("STATIC_ROOT")
MEDIA_URL = env.str("MEDIA_URL")
STATIC_URL = env.str("STATIC_URL")

KULTUS_PROVIDER_UI_BASE_URL = env.str("KULTUS_PROVIDER_UI_BASE_URL")
KULTUS_TEACHER_UI_BASE_URL = env.str("KULTUS_TEACHER_UI_BASE_URL")

ROOT_URLCONF = "palvelutarjotin.urls"
WSGI_APPLICATION = "palvelutarjotin.wsgi.application"

LANGUAGE_CODE = "fi"
LANGUAGES = (("fi", _("Finnish")), ("en", _("English")), ("sv", _("Swedish")))
TIME_ZONE = "Europe/Helsinki"
USE_I18N = True
USE_TZ = True
# Set to True to enable GraphiQL interface, this will overriden to True if DEBUG=True
ENABLE_GRAPHIQL = env("ENABLE_GRAPHIQL")

INSTALLED_APPS = [
    "helusers.apps.HelusersConfig",
    "helusers.apps.HelusersAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "corsheaders",
    "csp",
    "graphene_django",
    "rest_framework",
    "anymail",
    "mailer",
    "parler",
    "django_ilmoitin",
    "django_filters",
    "axes",
    "django_admin_listfilter_dropdown",
    # local apps under this line
    "utils",
    "organisations",
    "occurrences",
    "verification_token",
    "reports",
    "notification_importers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOWED_ORIGIN_REGEXES = env.list("CORS_ALLOWED_ORIGIN_REGEXES")
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL")


# Configure the default CSP rule for different source types
CSP_DEFAULT_SRC = [CSP.SELF]

# CSP_STYLE_SRC includes 'unsafe-inline' for inline styles added by `django-helusers`.
CSP_STYLE_SRC = [
    CSP.SELF,
    CSP.UNSAFE_INLINE,
    "cdn.jsdelivr.net",
    "blob:",
]

CSP_SCRIPT_SRC = [
    CSP.SELF,
    "cdn.jsdelivr.net",  # /graphql/ endpoint
    "blob:",
]

CSP_FONT_SRC = [
    CSP.SELF,
    "data:",  # /graphql/ endpoint uses "data:font/woff2"
]

CSP_IMG_SRC = [
    CSP.SELF,
    "blob:",
    "data:",
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "helusers.tunnistamo_oidc.TunnistamoOIDCAuth",
    "django.contrib.auth.backends.ModelBackend",
    "palvelutarjotin.oidc.GraphQLApiTokenAuthentication",
]
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"
AUTH_USER_MODEL = "organisations.User"
SOCIAL_AUTH_TUNNISTAMO_AUTH_EXTRA_ARGUMENTS = {"ui_locales": ""}

OIDC_API_TOKEN_AUTH = {
    # Audience that must be present in the token for it to be
    # accepted. Value must be agreed between your SSO service and your
    # application instance. Essentially this allows your application to
    # know that the token is meant to be used with it.
    # RequestJWTAuthentication supports multiple acceptable audiences,
    # so this setting can also be a list of strings.
    # This setting is required.
    "AUDIENCE": env.list("TOKEN_AUTH_ACCEPTED_AUDIENCE"),
    # Who we trust to sign the tokens. The library will request the
    # public signature keys from standard locations below this URL.
    # RequestJWTAuthentication supports multiple issuers, so this
    # setting can also be a list of strings.
    # Default is https://tunnistamo.hel.fi.
    "ISSUER": env.list("TOKEN_AUTH_AUTHSERVER_URL"),
    # The following can be used if you need certain scopes for any
    # functionality of the API. Usually this is not needed, as checking
    # the audience is enough. Default is False.
    "REQUIRE_API_SCOPE_FOR_AUTHENTICATION": env.bool("TOKEN_AUTH_REQUIRE_SCOPE_PREFIX"),
    # The name of the claim that is used to read in the scopes from the JWT.
    # Default is https://api.hel.fi/auth.
    # "API_AUTHORIZATION_FIELD": "scope_field",
    # The request will be denied if scopes don't contain anything starting
    # with the value provided here.
    "API_SCOPE_PREFIX": env.str("TOKEN_AUTH_ACCEPTED_SCOPE_PREFIX"),
    # In order to do the authentication RequestJWTAuthentication needs
    # some facts from the authorization server, mainly its public keys for
    # verifying the JWT's signature. This setting controls the time how long
    # authorization server configuration and public keys are "remembered".
    # The value is in seconds. Default is 24 hours.
    "OIDC_CONFIG_EXPIRATION_TIME": 600,
    # The name of the claim that is used to read in the scopes from the JWT.
    # Supports multiple fields as a list. If the field is deeper in the claims
    # use dot notation. e.g. "authorization.permissions.scopes"
    # Default is https://api.hel.fi/auth.
    "API_AUTHORIZATION_FIELD": env.str("TOKEN_AUTH_API_AUTHORIZATION_FIELD"),
}

OIDC_AUTH = {"OIDC_LEEWAY": 60 * 60}

SITE_ID = 1
SITE_URL = env.str("ENVIRONMENT_URL")

PARLER_LANGUAGES = {
    SITE_ID: ({"code": "fi"}, {"code": "sv"}, {"code": "en"}),
    "default": {
        "fallbacks": ["fi", "en", "sv"],  # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        "hide_untranslated": False,  # the default;
        # let .active_translations() return fallbacks too.
    },
}

PARLER_SUPPORTED_LANGUAGE_CODES = [x["code"] for x in PARLER_LANGUAGES[SITE_ID]]

PARLER_REQUIRE_DEFAULT_TRANSLATION = False

GRAPHENE = {
    "SCHEMA": "palvelutarjotin.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
    "DJANGO_CHOICE_FIELD_ENUM_CONVERT": True,
}

GRAPHQL_JWT = {"JWT_AUTH_HEADER_PREFIX": "Bearer"}

PALVELUTARJOTIN_QUERY_MAX_DEPTH = 12
LINKED_EVENTS_API_CONFIG = {
    "ROOT": env.str("LINKED_EVENTS_API_ROOT"),
    "API_KEY": env.str("LINKED_EVENTS_API_KEY"),
    "DATA_SOURCE": env.str("LINKED_EVENTS_DATA_SOURCE"),
}

SERVICEMAP_API_CONFIG = {"ROOT": env.str("SERVICEMAP_API_ROOT")}

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hour after locked out, user will be able to attempt login

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django": {"handlers": ["console"], "level": "ERROR"}},
}

if DEBUG is True:
    LOGGING["loggers"] = {
        "django": {"handlers": ["console"], "level": "WARNING"},
        "occurrences": {"handlers": ["console"], "level": "DEBUG"},
        "organisations": {"handlers": ["console"], "level": "DEBUG"},
        "palvelutarjotin": {"handlers": ["console"], "level": "DEBUG"},
    }

CAPTCHA_ENABLED = env.bool("CAPTCHA_ENABLED")
RECAPTCHA_SECRET_KEY = env.str("RECAPTCHA_SECRET_KEY")
RECAPTCHA_VALIDATION_URL = "https://www.google.com/recaptcha/api/siteverify"
ENABLE_SUMMARY_REPORT = env.bool("ENABLE_SUMMARY_REPORT")

KEYWORD_SET_ID_MAPPING = {
    "CATEGORY": env.str("KEYWORD_SET_CATEGORY_ID"),
    "ADDITIONAL_CRITERIA": env.str("KEYWORD_SET_ADDITIONAL_CRITERIA_ID"),
    "ACTIVITIES": env.str("KEYWORD_SET_ACTIVITIES_ID"),
    "TARGET_GROUP": env.str("KEYWORD_SET_TARGET_GROUP_ID"),
}

VERIFICATION_TOKEN_URL_MAPPING = {
    "occurrences.enrolment.CANCELLATION": f"{KULTUS_TEACHER_UI_BASE_URL}"
    + "{lang}/enrolments/cancel/{unique_id}",
    "occurrences.enrolment.CANCELLATION.confirmation": f"{KULTUS_TEACHER_UI_BASE_URL}"
    + "{lang}/enrolments/cancel/{unique_id}?token={token}",
}

MAX_UPLOAD_SIZE = 2621440  # 2MB

PERSONAL_DATA_RETENTION_PERIOD_MONTHS = env("PERSONAL_DATA_RETENTION_PERIOD_MONTHS")

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
local_settings_path = os.path.join(checkout_dir(), "local_settings.py")
if os.path.exists(local_settings_path):
    with open(local_settings_path) as fp:
        code = compile(fp.read(), local_settings_path, "exec")
    exec(code, globals(), locals())

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

NOTIFICATIONS_IMPORTER = (
    "notification_importers.notification_importer.NotificationFileImporter"
)

UPDATE_LAST_LOGIN = {
    "ENABLED": env.bool("UPDATE_LAST_LOGIN_ENABLED"),
    "UPDATE_INTERVAL_MINUTES": env.int("UPDATE_LAST_LOGIN_INTERVAL_MINUTES"),
}

# release information
APP_RELEASE = env("APP_RELEASE")
# get build time from a file in docker image
APP_BUILD_TIME = datetime.fromtimestamp(os.path.getmtime(__file__))

GDPR_API_MODEL = AUTH_USER_MODEL
GDPR_API_QUERY_SCOPE = env("GDPR_API_QUERY_SCOPE")
GDPR_API_DELETE_SCOPE = env("GDPR_API_DELETE_SCOPE")
GDPR_API_MODEL_LOOKUP = "uuid"
GDPR_API_URL_PATTERN = "v1/user/<uuid:uuid>"
GDPR_API_USER_PROVIDER = "gdpr.service.get_user"
GDPR_API_DELETER = "gdpr.service.delete_data"
# By default, the migration logic is configured to support migrating users
# from Tunnistamo AD authentication to Keycloak AD authentication.
# The migration should be tested by the service before enabling it in production.
# This migration logic most likely shouldn't be configured for other
# authentication methods besides AD (i.e. staff/admin) users.
#
# When transitioning from one authentication provider to another,
# it's possible to migrate the old user data for the new user with a different UUID.
# Migration is done by finding the old user instance and replacing its UUID
# with the new one from the token payload. So instead of creating a new user
# instance, we update the old one. Migration happens one user at a time upon login.
# Feature can be configured using the following settings.
# HELUSERS_USER_MIGRATE_ENABLED: Enable the feature. Defaults to False.
# HELUSERS_USER_MIGRATE_EMAIL_DOMAINS: Whitelisted email domains for migration.
#   Defaults to ["hel.fi"].
# HELUSERS_USER_MIGRATE_AMRS which authentication methods are used for migration.
#   Defaults to ["helsinkiad"].
HELUSERS_USER_MIGRATE_ENABLED = env.bool("HELUSERS_USER_MIGRATE_ENABLED", True)
HELUSERS_BACK_CHANNEL_LOGOUT_ENABLED = env.bool(
    "HELUSERS_BACK_CHANNEL_LOGOUT_ENABLED", True
)
