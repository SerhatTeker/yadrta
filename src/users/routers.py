from rest_framework.routers import DefaultRouter

from src.users.views import UserCreateViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"users", UserCreateViewSet)
