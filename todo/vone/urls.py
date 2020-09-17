from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"todo", views.TodoViewSet)
router.register(r"tag", views.TagViewSet)
router.register(r"category", views.CategoryViewSet)


# disabled
api_views = [
    path("todos/", views.TodoListView.as_view()),
    path("todos/<int:id>", views.TodoDetailView.as_view()),
]

model_view_sets = [path("", include(router.urls))]

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

urlpatterns = model_view_sets + swagger
