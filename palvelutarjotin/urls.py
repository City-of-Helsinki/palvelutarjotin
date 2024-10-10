import json

from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import include, path
from django.utils.translation import gettext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from helusers.admin_site import admin

from common.utils import get_api_version
from palvelutarjotin import __version__
from palvelutarjotin.views import SentryGraphQLView

admin.site.index_title = " ".join([gettext("Kultus API"), get_api_version()])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("reports/", include("reports.urls")),
    path("pysocial/", include("social_django.urls", namespace="social")),
    path("helauth/", include("helusers.urls")),
    path("gdpr-api/", include("helsinki_gdpr.urls")),
    path(
        "graphql",
        csrf_exempt(
            SentryGraphQLView.as_view(
                graphiql=settings.ENABLE_GRAPHIQL or settings.DEBUG
            )
        ),
    ),
]


#
# Kubernetes liveness & readiness probes
#
def healthz(*args, **kwargs):
    return HttpResponse(status=200)


def readiness(*args, **kwargs):
    return HttpResponse(status=200)


@require_GET
def version(*args, **kwargs):
    response_json = {
        "status": "ok",
        "release": settings.APP_RELEASE,
        "packageVersion": __version__,
        "commitHash": settings.COMMIT_HASH.decode("utf-8"),
        "buildTime": settings.APP_BUILD_TIME.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    }
    return HttpResponse(json.dumps(response_json), status=200)


urlpatterns += [
    path("healthz", healthz),
    path("readiness", readiness),
    path("api/version", version),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
