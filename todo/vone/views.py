# from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .models import Category, Tag, Task
from .serializers import TaskSerializer


class TodoListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TodoDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Task.objects.all()
    # permission_classes = (permissions.AllowAny,)
    serializer_class = TaskSerializer
