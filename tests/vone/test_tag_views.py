import logging

from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from src.vone.models import Tag

from .factories import TagFactory
from .utils import user_id_to_hex

fake = Faker()
LOGGER = logging.getLogger(__name__)


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
        self.tag = TagFactory()
        self.url_detail = reverse("tag-detail", kwargs={"pk": self.tag.pk})
        # User
        self.user = self.tag.created_by
        self.api_authentication()
        # API
        self.payload = self.set_payload()
        self.response = self.set_response()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def set_payload(self):
        return {"name": self.tag.name, "created_by": self.user.pk}

    def _set_response(self, url, payload=None, name=None, created_by=None):
        if not payload:
            payload = {"name": name, "created_by": created_by}

        return self.client.post(url, payload)

    def set_response(self):
        """Default response for cls"""
        response = self._set_response(url=self.url, payload=self.payload)
        return response

    def test_get_request_returns_a_givzen_tag(self):
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
        # LOGGER.info(f"response before delete: {self.response}")
        response = self.client.delete(self.url_detail)
        # LOGGER.info(f"response after delete: {response}")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
