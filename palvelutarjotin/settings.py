import os
import subprocess

import environ
import sentry_sdk
from django.utils.translation import ugettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

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
    ALLOWED_HOSTS=(list, []),
    USE_X_FORWARDED_HOST=(bool, False),
    DATABASE_URL=(
        str,
        "postgres://palvelutarjotin:palvelutarjotin@localhost/palvelutarjotin",
    ),
    CACHE_URL=(str, "locmemcache://"),
    MAILER_EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
    DEFAULT_FROM_EMAIL=(str, "no-reply@hel.ninja"),
    ILMOITIN_TRANSLATED_FROM_EMAIL=(dict, {}),
    MAIL_MAILGUN_KEY=(str, ""),
    MAIL_MAILGUN_DOMAIN=(str, ""),
    MAIL_MAILGUN_API=(str, ""),
    SENTRY_DSN=(str, ""),
    SENTRY_ENVIRONMENT=(str, ""),
    CORS_ORIGIN_WHITELIST=(list, []),
    CORS_ORIGIN_ALLOW_ALL=(bool, False),
    TOKEN_AUTH_ACCEPTED_AUDIENCE=(str, "https://api.hel.fi/auth/palvelutarjotin"),
    TOKEN_AUTH_ACCEPTED_SCOPE_PREFIX=(str, "palvelutarjotin"),
    TOKEN_AUTH_REQUIRE_SCOPE_PREFIX=(bool, True),
    TOKEN_AUTH_AUTHSERVER_URL=(str, ""),
    ILMOITIN_QUEUE_NOTIFICATIONS=(bool, False),
    DEFAULT_FILE_STORAGE=(str, "django.core.files.storage.FileSystemStorage"),
    GS_BUCKET_NAME=(str, ""),
    STAGING_GCS_BUCKET_CREDENTIALS=(str, ""),
    GS_DEFAULT_ACL=(str, "publicRead"),
    GS_FILE_OVERWRITE=(bool, False),
    AZURE_ACCOUNT_NAME=(str, ""),
    AZURE_ACCOUNT_KEY=(str, ""),
    AZURE_CONTAINER=(str, ""),
    ENABLE_GRAPHIQL=(bool, False),
    LINKED_EVENTS_API_ROOT=(str, "https://api.hel.fi/linkedevents/v1/"),
    LINKED_EVENTS_API_KEY=(str, ""),
    LINKED_EVENTS_DATA_SOURCE=(str, "palvelutarjotin"),
)

if os.path.exists(env_file):
    env.read_env(env_file)

BASE_DIR = str(checkout_dir)

DEBUG = env.bool("DEBUG")
SECRET_KEY = env.str("SECRET_KEY")
if DEBUG and not SECRET_KEY:
    SECRET_KEY = "xxx"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
USE_X_FORWARDED_HOST = env.bool("USE_X_FORWARDED_HOST")

DATABASES = {"default": env.db()}

CACHES = {"default": env.cache()}

if env.str("DEFAULT_FROM_EMAIL"):
    DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
if env("MAIL_MAILGUN_KEY"):
    ANYMAIL = {
        "MAILGUN_API_KEY": env("MAIL_MAILGUN_KEY"),
        "MAILGUN_SENDER_DOMAIN": env("MAIL_MAILGUN_DOMAIN"),
        "MAILGUN_API_URL": env("MAIL_MAILGUN_API"),
    }
EMAIL_BACKEND = "mailer.backend.DbBackend"
MAILER_EMAIL_BACKEND = env.str("MAILER_EMAIL_BACKEND")
ILMOITIN_TRANSLATED_FROM_EMAIL = env("ILMOITIN_TRANSLATED_FROM_EMAIL")
ILMOITIN_QUEUE_NOTIFICATIONS = env("ILMOITIN_QUEUE_NOTIFICATIONS")

try:
    REVISION = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
except Exception:
    REVISION = "n/a"

sentry_sdk.init(
    dsn=env.str("SENTRY_DSN"),
    release=REVISION,
    environment=env("SENTRY_ENVIRONMENT"),
    integrations=[DjangoIntegration()],
)

MEDIA_ROOT = env("MEDIA_ROOT")
STATIC_ROOT = env("STATIC_ROOT")
MEDIA_URL = env.str("MEDIA_URL")
STATIC_URL = env.str("STATIC_URL")

# For staging env, we use Google Cloud Storage
DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE")
if DEFAULT_FILE_STORAGE == "storages.backends.gcloud.GoogleCloudStorage":
    GS_BUCKET_NAME = env("GS_BUCKET_NAME")
    GOOGLE_APPLICATION_CREDENTIALS = env("STAGING_GCS_BUCKET_CREDENTIALS")
    GS_DEFAULT_ACL = env("GS_DEFAULT_ACL")
    GS_FILE_OVERWRITE = env("GS_FILE_OVERWRITE")
# For prod, it's Azure Storage
elif DEFAULT_FILE_STORAGE == "storages.backends.azure_storage.AzureStorage":
    AZURE_ACCOUNT_NAME = env("AZURE_ACCOUNT_NAME")
    AZURE_ACCOUNT_KEY = env("AZURE_ACCOUNT_KEY")
    AZURE_CONTAINER = env("AZURE_CONTAINER")

ROOT_URLCONF = "palvelutarjotin.urls"
WSGI_APPLICATION = "palvelutarjotin.wsgi.application"

LANGUAGE_CODE = "fi"
LANGUAGES = (("fi", _("Finnish")), ("en", _("English")), ("sv", _("Swedish")))
TIME_ZONE = "Europe/Helsinki"
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Set to True to enable GraphiQL interface, this will overriden to True if DEBUG=True
ENABLE_GRAPHIQL = env("ENABLE_GRAPHIQL")

INSTALLED_APPS = [
    "helusers",
    "helusers.apps.HelusersAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "graphene_django",
    "anymail",
    "mailer",
    "parler",
    "django_ilmoitin",
    "django_filters",
    "axes",
    # local apps under this line
    "utils",
    "organisations",
    "occurrences",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
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

CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL")

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
    "palvelutarjotin.oidc.GraphQLApiTokenAuthentication",
]

AUTH_USER_MODEL = "organisations.User"

OIDC_API_TOKEN_AUTH = {
    "AUDIENCE": env.str("TOKEN_AUTH_ACCEPTED_AUDIENCE"),
    "API_SCOPE_PREFIX": env.str("TOKEN_AUTH_ACCEPTED_SCOPE_PREFIX"),
    "ISSUER": env.str("TOKEN_AUTH_AUTHSERVER_URL"),
    "REQUIRE_API_SCOPE_FOR_AUTHENTICATION": env.bool("TOKEN_AUTH_REQUIRE_SCOPE_PREFIX"),
}

OIDC_AUTH = {"OIDC_LEEWAY": 60 * 60}

SITE_ID = 1

PARLER_LANGUAGES = {SITE_ID: ({"code": "fi"}, {"code": "sv"}, {"code": "en"})}

PARLER_SUPPORTED_LANGUAGE_CODES = [x["code"] for x in PARLER_LANGUAGES[SITE_ID]]

PARLER_REQUIRE_DEFAULT_TRANSLATION = False

GRAPHENE = {
    "SCHEMA": "palvelutarjotin.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

GRAPHQL_JWT = {"JWT_AUTH_HEADER_PREFIX": "Bearer"}

PALVELUTARJOTIN_QUERY_MAX_DEPTH = 12
LINKED_EVENTS_API_CONFIG = {
    "ROOT": env.str("LINKED_EVENTS_API_ROOT"),
    "API_KEY": env.str("LINKED_EVENTS_API_KEY"),
    "DATA_SOURCE": env.str("LINKED_EVENTS_DATA_SOURCE"),
}

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hour after locked out, user will be able to attempt login

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django": {"handlers": ["console"], "level": "ERROR"}},
}

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
local_settings_path = os.path.join(checkout_dir(), "local_settings.py")
if os.path.exists(local_settings_path):
    with open(local_settings_path) as fp:
        code = compile(fp.read(), local_settings_path, "exec")
    exec(code, globals(), locals())
