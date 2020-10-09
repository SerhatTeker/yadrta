from rest_framework.routers import DefaultRouter

from src.users.routers import router as user_router
from src.vone.routers import router as vone_router


class DefaultRouter(DefaultRouter):
    """
    Extend `DefaultRouter` class to add a method for extending url routes from another router.
    """

    def extend(self, router):
        """
        Extend the routes with url routes of the passed in router.

        :param router: :class: DefaultRouter instance containing route definitions.
        :type router: class:`rest_framework.routes.DefaultRouter`
        :return: None
        """
        self.registry.extend(router.registry)


router = DefaultRouter()
router.extend(user_router)
router.extend(vone_router)
