from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views as auth_views

from .routers import router

users_urls = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("api-token-auth/", auth_views.obtain_auth_token, name="obtain_auth_token"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

drf_urls = [
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
]

version = "v1"
api_urls = [
    path(f"api/{version}/", include(router.urls)),
    # docs
    path(f"api{version}/doc/", include("src.vone.urls"))
]

urlpatterns = users_urls \
    + drf_urls \
    + api_urls \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
