import logging

import factory
from rest_framework import status
from rest_framework.test import APITestCase

from src.core.utils.tests import APIClientMixin, user_id_to_hex
from src.vone.models import Category
from tests.users.factories import UserFactory

from .factories import CategoryFactory, fake

LOGGER = logging.getLogger(__name__)


class BaseTestClass(APITestCase):
    def setUp(self):
        # User
        self.user = None
        # "category" : str
        self.model_str = "category"
        # categoryFactory : obj
        self.factory_class = CategoryFactory
        # Model
        self.model_data = factory.build(dict, FACTORY_CLASS=self.factory_class)
        # API
        self.payload = None
        self.response = None

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")


class TestCategoryListAPIView(BaseTestClass, APIClientMixin):
    """
    Tests /category detail operations.
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        self.user = UserFactory()
        self.api_authentication()
        self.url = self.get_model_url_list()
        self.payload = self.set_payload()
        self.response = self.client_post()

    def test_post_request_with_no_data_fails(self):
        payload = {}
        response = self.client.post(self.url, payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_request_with_valid_data_succeeds(self):
        self.assertEqual(status.HTTP_201_CREATED, self.response.status_code)

    def test_bulk_category_create_fail_with_different_user(self):
        # create 2 another new categorys
        self.factory_class.create_batch(2)
        response = self.client_get()
        self.assertEqual(response.data.get("count"), 1)

    def test_bulk_category_create(self):
        # create 2 another new categorys
        # self.factory_class.create_batch(2, craeted_by=self.user)
        self.factory_class.create_batch(size=2, created_by=self.user)
        response = self.client_get()
        self.assertGreaterEqual(response.data.get("count"), 3)


class TestCategoryDetailAPIView(BaseTestClass, APIClientMixin):
    """
    Tests /category detail operations.
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        self.category = CategoryFactory()
        # LOGGER.info(f"category: {self.category}")
        self.user = self.category.created_by
        self.api_authentication()
        self.url = self.get_obj_url(object_pk=self.category.id)

    def test_get_request_returns_a_given_category(self):
        # From APIClient
        response_obj_name = self.client_get().data.get("name")
        # From factory_class
        obj_name = self.category.name
        self.assertEqual(response_obj_name, obj_name)

    def test_get_request_returns_user_id(self):
        user_hex = self.client_get().data.get("created_by").hex
        user_id = user_id_to_hex(self.user.id)
        self.assertEqual(user_hex, user_id)

    def test_category_object_update(self):
        name = fake.word()
        payload = self._set_payload(name=name, created_by=self.user.id)
        response = self.client.put(self.url, payload)
        response_data = response.data.get("name")

        category = Category.objects.get(id=self.category.id)
        self.assertEqual(response_data, category.name)

    def test_category_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    # def test_todo_object_delete_authorization(self):
    #     """
    #     Test to verify that put call with different user token
    #     """
    #     new_user = UserFactory()
    #     new_category = CategoryFactory()
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Token {new_user.auth_token}")
    #     response = self.client.get(self.get_obj_url(new_category.id))
    #     LOGGER.info(f"response: {response}")
    #     LOGGER.info(f"response.data: {response.data}")
    #     LOGGER.info(f"response.dict: {response.__dict__}")
    #     # self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
    #     self.assertNotEquals(new_user.id, new_category.created_by.id)
