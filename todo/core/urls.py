from django.contrib import admin
from django.urls import include, path

from todo.vone.views import index

# django defaults
# -------------------------------------------------------------------------------
default = [
    # redirect to /api/v1/
    path("", index),
    # django admin
    path("admin/", admin.site.urls)
]

# django-rest-framework
# -------------------------------------------------------------------------------
drf = [
    # Auth
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]

# API v1
# -------------------------------------------------------------------------------
api_v1 = [path("api/v1/", include("todo.vone.urls"))]

urlpatterns = default + drf + api_v1
