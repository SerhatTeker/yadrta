from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Category, Tag, Task
from .serializers import CategorySerializer, TagSerializer, TaskSerializer

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


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
