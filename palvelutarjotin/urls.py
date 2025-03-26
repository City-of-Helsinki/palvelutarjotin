import json

from csp.decorators import csp_update
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import include, path, re_path
from django.utils.translation import gettext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from helusers.admin_site import admin

from common.utils import get_api_version
from palvelutarjotin import __version__
from palvelutarjotin.consts import CSP
from palvelutarjotin.views import SentryGraphQLView

admin.site.index_title = " ".join([gettext("Kultus API"), get_api_version()])

IS_GRAPHIQL_ENABLED = settings.ENABLE_GRAPHIQL or settings.DEBUG


# Add unsafe-inline to enable GraphiQL interface at /graphql/
@csp_update(
    SCRIPT_SRC=settings.CSP_SCRIPT_SRC
    + ([CSP.UNSAFE_INLINE] if IS_GRAPHIQL_ENABLED else [])
)
@csrf_exempt
def graphql_view(request, *args, **kwargs):
    return SentryGraphQLView.as_view(graphiql=IS_GRAPHIQL_ENABLED)(
        request, *args, **kwargs
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("reports/", include("reports.urls")),
    path("pysocial/", include("social_django.urls", namespace="social")),
    path("helauth/", include("helusers.urls")),
    path("gdpr-api/", include("helsinki_gdpr.urls")),
    re_path(r"^graphql/?$", graphql_view),
]


#
# Kubernetes liveness & readiness probes
#
@require_http_methods(["GET", "HEAD"])
def healthz(*args, **kwargs):
    return HttpResponse(status=200)


@require_http_methods(["GET", "HEAD"])
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
