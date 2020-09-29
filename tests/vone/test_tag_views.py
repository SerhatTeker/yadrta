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
        # "tag" : str
        self.model = "tag"
        # TagFactory : obj
        self.factory_class = TagFactory
        # Model
        self.url = reverse(f"{self.model}-list")
        self.tag_data = factory.build(dict, FACTORY_CLASS=self.factory_class)
        self.url_detail = reverse(
            f"{self.model}-detail", kwargs={"pk": self.tag_data.get("id")}
        )
        # API
        self.payload = None
        self.response = None

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def _set_payload(self, name=None, created_by=None):
        if name and created_by is None:
            name = self.tag_data.get("name")
            created_by = self.user.pk

        payload = {"name": name, "created_by": created_by}

        return payload

    def set_payload(self):
        """Default payload for cls"""
        # payload = {"name": self.tag_data.get("name"), "created_by": self.user.pk}
        name = self.tag_data.get("name")
        created_by = self.user.pk

        return self._set_payload(name=name, created_by=created_by)

    def client_get(self, url=None):
        if not url:
            url = self.url

        return self.client.get(url)

    def client_post(self, url=None, payload=None):
        response = None

        if url and payload is None:
            url = self.url
            payload = self.payload

        response = self.client.post(self.url, self.payload)

        return response


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


class TestTagDetailAPIView(BaseTestClass):
    """
    Tests /tag detail operations.
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        self.payload = self.set_payload()
        self.response = self.client_post()

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
        response = self.client.delete(self.url_detail)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_bulk_tag_create(self):
        # create 2 another new tags
        self.factory_class.create_batch(2)
        response = self.client_get()
        LOGGER.info(f"responses count: {response.data.get('count')}")
        self.assertGreaterEqual(response.data.get("count"), 2)


class TestTrialBaseTestClass(BaseTestClass):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.payload = self.set_payload()

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_request_tag_name(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(self.tag_data.get("name"), response.data.get("name"))
