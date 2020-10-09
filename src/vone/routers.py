from rest_framework.routers import DefaultRouter

from src.vone.views import CategoryViewSet, TagViewSet, TodoViewSet

router = DefaultRouter()
router.register(r"todo", TodoViewSet)
router.register(r"tag", TagViewSet)
router.register(r"category", CategoryViewSet)
