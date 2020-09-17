from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'todo', views.TodoViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'category', views.CategoryViewSet)

api_views = [
    path('todos/', views.TodoListView.as_view()),
    path('todos/<int:id>', views.TodoDetailView.as_view()),
]

model_view_sets = [
    path('', include(router.urls)),
]

urlpatterns = model_view_sets
