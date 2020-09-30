import logging

import factory
from rest_framework import status
from rest_framework.test import APITestCase

from src.core.utils.tests import APIClientUtils, user_id_to_hex
from src.vone.models import Task
from tests.users.factories import UserFactory

from .factories import CategoryFactory, TagFactory, TaskFactory, fake

LOGGER = logging.getLogger(__name__)


class BaseTestClass(APITestCase):
    def setUp(self):
        # User
        self.user = None
        # "task" : str
        self.model_str = "task"
        # TaskFactory : obj
        self.factory_class = TaskFactory
        # Model
        self.model_data = factory.build(dict, FACTORY_CLASS=self.factory_class)
        # API
        self.payload = None
        self.response = None

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")


class TestTaskListAPIView(BaseTestClass, APIClientUtils):
    """
    Tests /task detail operations.
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        # Overwrite Task related fields
        self.user = UserFactory()
        self.api_authentication()
        self.tag = TagFactory()
        self.category = CategoryFactory()
        # ------------------------------------------------==
        self.url = self.get_model_url_list()
        self.payload = self.set_todo_payload()
        self.response = self.client_post()

    def test_post_request_with_no_data_fails(self):
        payload = {}
        response = self.client.post(self.url, payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_request_with_valid_data_succeeds(self):
        self.assertEqual(status.HTTP_201_CREATED, self.response.status_code)

    def test_bulk_task_create(self):
        # create 2 another new tasks
        self.factory_class.create_batch(2)
        response = self.client_get()
        self.assertGreaterEqual(response.data.get("count"), 3)


class TestTaskDetailAPIView(BaseTestClass, APIClientUtils):
    """
    Tests /task detail operations.
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        self.task = TaskFactory()
        # LOGGER.info(f"task: {self.task}")
        self.user = self.task.created_by
        self.api_authentication()
        self.tag = TagFactory()
        self.category = CategoryFactory()
        self.url = self.get_obj_url(object_pk=self.task.id)

    def test_get_request_returns_a_given_task(self):
        # From APIClient
        response_obj_name = self.client_get().data.get("title")
        # From factory_class
        obj_name = self.task.title
        self.assertEqual(response_obj_name, obj_name)

    def test_get_request_returns_user_id(self):
        user_hex = self.client_get().data.get("created_by").hex
        user_id = user_id_to_hex(self.user.id)
        self.assertEqual(user_hex, user_id)

    def test_task_object_update(self):
        payload = {"title": fake.word(), "created_by": self.user.id}
        response = self.client.put(self.url, payload)
        response_data = response.data.get("title")

        task = Task.objects.get(id=self.task.id)
        self.assertEqual(response_data, task.title)

    def test_task_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
