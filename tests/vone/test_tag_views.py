import logging

import factory
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

# from src.users.models import User
from src.vone.models import Tag
from tests.users.factories import UserFactory

from .factories import TagFactory
from .utils import user_id_to_hex

fake = Faker()
LOGGER = logging.getLogger(__name__)


class BaseTestClass(APITestCase):
    def setUp(self):
        # User
        self.user = UserFactory()
        self.api_authentication()
        self.model = "tag"
        # Tag
        self.url = reverse(f"{self.model}-list")
        self.tag_data = factory.build(dict, FACTORY_CLASS=TagFactory)
        self.url_detail = reverse(f"{self.model}-detail", kwargs={"pk": self.tag_data.get("id")})
        # API
        self.payload = None
        self.response = None

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def get_payload(self):
        payload = {"name": self.tag_data.get("name"), "created_by": self.user.pk}

        return payload

    def get_response(self, url=None):
        if not url:
            url = self.url

        return self.client.get(url)


class TestTagListAPIView(APITestCase):
    """
    Tests /tag list operations.
    """

    def setUp(self):
        self.url = reverse("tag-list")
        self.tag = TagFactory()
        self.user = self.tag.created_by
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def test_post_request_with_no_data_fails(self):
        payload = {}
        response = self.client.post(self.url, payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_request_with_valid_data_succeeds(self):
        payload = {"name": "newthing", "created_by": self.user.pk}
        response = self.client.post(self.url, payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class TestTagCreateAPIView(APITestCase):
    """
    Tests /tag create operations.
    """

    def setUp(self):
        self.url = reverse("tag-list")
        self.tag = TagFactory()
        self.user = self.tag.created_by
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def test_create_tag(self):
        payload = {"name": self.tag.name, "created_by": self.user.pk}
        response = self.client.post(self.url, payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class TestTagDetailAPIView(APITestCase):
    """
    Tests /tag detail operations.
    """

    def setUp(self):
        # Tag
        self.url = reverse("tag-list")
        self.user = UserFactory()
        self.tag = factory.build(dict, FACTORY_CLASS=TagFactory)
        self.url_detail = reverse("tag-detail", kwargs={"pk": self.tag.pk})
        # User
        self.user = self.tag.created_by
        self.api_authentication()
        # API
        self.payload = self.set_payload()
        self.response = self.set_response()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def get_response(self):
        return self.client.get(self.url)

    def set_payload(self):
        return {"name": self.tag.name, "created_by": self.user.pk}

    def _set_response(self, payload=None, name=None, created_by=None):
        if not payload:
            payload = {"name": name, "created_by": created_by}

        return self.client.post(self.url, payload)

    def set_response(self):
        """Default response for cls"""
        response = self._set_response(payload=self.payload)
        return response

    def test_get_request_returns_a_given_tag(self):
        self.assertEqual(self.response.data.get("name"), self.tag.name)

    def test_get_request_returns_user_id(self):
        self.assertEqual(
            self.response.data.get("created_by").hex, user_id_to_hex(self.user.id)
        )

    def test_tag_object_update(self):
        response = self.client.put(self.url_detail, self.payload)
        tag = Tag.objects.get(id=self.tag.id)
        self.assertEqual(response.data.get("name"), tag.name)

    def test_tag_object_delete(self):
        # LOGGER.info(f"self response data before delete: {self.response.data}")
        # response = self.client.get(self.url)
        # LOGGER.info(f"---response data before delete: {response.data}")
        # LOGGER.info(f"responses name: {self.response.data.get('name')}")
        # LOGGER.info(f"responses count: {self.response.data.get('count')}")
        response = self.client.delete(self.url_detail)
        # LOGGER.info(f"response after delete: {response}")
        # LOGGER.info(f"responses count: {self.response.data.get('count')}")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_bulk_tag_create(self):
        # create 2 another new tags
        TagFactory.create_batch(2)
        response = self.get_response()
        LOGGER.info(f"responses count: {response.data.get('count')}")
        self.assertGreaterEqual(response.data.get("count"), 2)


class TestTrialBaseTestClass(BaseTestClass):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.payload = self.get_payload()

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_request_tag_name(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(self.tag_data.get("name"), response.data.get("name"))
