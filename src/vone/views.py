from django.http import HttpResponseRedirect
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from src.core.utils.views import BaseModelViewSetWithTracking, EnablePartialUpdateMixin

from .models import Category, Tag, Task
from .serializers import CategorySerializer, TagSerializer, TaskSerializer

# inactive
def index(request):
    """ Redirect $home_url `/` to `/api/v1/` """
    return HttpResponseRedirect("/api/v1/")


# ViewSets
# ------------------------------------------------------------------------------


class CategoryViewSet(BaseModelViewSetWithTracking):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(BaseModelViewSetWithTracking):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TodoViewSet(EnablePartialUpdateMixin, BaseModelViewSetWithTracking):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# OpenAPI schema
# ------------------------------------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="YADRTA API",
        default_version="v1.0.0",
        description="Yet Another Djando REST Todo App using django rest and django with OpenAPI Specification.",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="serhatteker@gmail.com"),
        license=openapi.License(name="BSD-3-Clause License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)
