from django.urls import path, re_path

from . import views

swagger = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        views.schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        views.schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        views.schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

urlpatterns = swagger
