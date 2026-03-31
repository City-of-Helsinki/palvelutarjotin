from csp.constants import UNSAFE_INLINE as CSP_UNSAFE_INLINE
from csp.decorators import csp_update
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.utils.translation import gettext
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)
from helusers.admin_site import admin

from common.utils import get_api_version
from palvelutarjotin.views import SentryGraphQLView

admin.site.index_title = " ".join([gettext("Kultus API"), get_api_version()])

IS_GRAPHIQL_ENABLED = settings.ENABLE_GRAPHIQL or settings.DEBUG


# Add unsafe-inline to enable GraphiQL interface at /graphql/
@csp_update(
    {
        "script-src": settings.CONTENT_SECURITY_POLICY["DIRECTIVES"]["script-src"]
        + ([CSP_UNSAFE_INLINE] if IS_GRAPHIQL_ENABLED else []),
    }
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


urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


# Kubernetes liveness & readiness probes
urlpatterns += [path("", include("helsinki_health_endpoints.urls"))]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
