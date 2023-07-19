import json
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import include, path
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from helusers.admin_site import admin
from palvelutarjotin import __version__

from common.utils import get_api_version
from palvelutarjotin.views import SentryGraphQLView

admin.site.index_title = " ".join([ugettext("Kultus API"), get_api_version()])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("reports/", include("reports.urls")),
    path("pysocial/", include("social_django.urls", namespace="social")),
    path("helauth/", include("helusers.urls")),
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
    response_json = {
        "status": "ok",
        "release": settings.BUILD_INFO_RELEASE,
        "packageVersion": __version__,
        "commitHash": settings.REVISION.decode("utf-8"),
        "buildTime": settings.BUILD_INFO_BUILDTIME.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    }
    return HttpResponse(json.dumps(response_json), status=200)


urlpatterns += [path("healthz", healthz), path("readiness", readiness)]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
