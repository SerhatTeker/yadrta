from django.http import HttpResponseRedirect
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from src.core.utils.views import EnablePartialUpdateMixin

from .models import Category, Tag, Task
from .serializers import CategorySerializer, TagSerializer, TaskSerializer


def index(request):
    """ Redirect $home_url `/` to `/api/v1/` """
    return HttpResponseRedirect("/api/v1/")


# APIViews
# ------------------------------------------------------------------------------


class TodoListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TodoDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Task.objects.all()
    # permission_classes = (permissions.AllowAny,)
    serializer_class = TaskSerializer


# ViewSets
# ------------------------------------------------------------------------------


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TodoViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# OpenAPI schema
# ------------------------------------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Todo API",
        default_version="v1",
        description="Django REST Todo App",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="serhatteker@gmail.com"),
        license=openapi.License(name="BSD-3-Clause License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)
