from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import path
from django.utils.translation import ugettext
from helusers.admin_site import admin

from common.utils import get_api_version

admin.site.index_title = " ".join(
    [ugettext("Palvelutarjotin backend"), get_api_version()]
)

urlpatterns = [
    path("admin/", admin.site.urls),
]


#
# Kubernetes liveness & readiness probes
#
def healthz(*args, **kwargs):
    return HttpResponse(status=200)


def readiness(*args, **kwargs):
    return HttpResponse(status=200)


urlpatterns += [path("healthz", healthz), path("readiness", readiness)]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
