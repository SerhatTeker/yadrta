from uuid import UUID

from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from src.vone.models import Tag
from tests.vone.factories import TagFactory

fake = Faker()


def user_id_to_hex(uuid: str) -> str:
    """
    Turn uuid4 with hashes to hex:
    From    :  8791f25b-d4ca-4f10-8f60-407a507edefe
    To      :  8791f25bd4ca4f108f60407a507edefe
    """

    return UUID(uuid).hex


# Tag
# ------------------------------------------------------------------------------


class TestTagListView(APITestCase):
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
        # print(f"response __dict__: {response.__dict__}")
        # print(f"response content: {response.content}")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class TestTagDetailView(APITestCase):
    """
    Tests /tag list operations.
    """

    def setUp(self):
        self.url = reverse("tag-list")
        # try_two
        self.tag = TagFactory()
        print(f"tag: {self.tag}")
        print(f"created_by: {self.tag.created_by}")
        self.user = self.tag.created_by
        # try_one
        # self.user_data = factory.build(dict, FACTORY_CLASS=UserFactory)
        # self.tag_data = factory.build(dict, FACTORY_CLASS=TagFactory)
        # print(f"tag_data: {self.tag_data}")
        # print(f"user obj: {self.tag_data.get('created_by')}")
        # print(f"user.id: {self.tag_data.get('created_by').id}")
        # self.user = self.tag_data.get("created_by")
        # self.user = User.objects.get(pk=self.tag_data.get("created_by").id)
        self.api_authentication()
        self.response = self.set_response()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def set_response(self):
        payload = {"name": self.tag.name, "created_by": self.user.pk}
        return self.client.post(self.url, payload)

    def test_get_request_returns_a_given_tag(self):
        self.assertEqual(self.response.data.get("name"), self.tag.name)

    def test_get_request_returns_user_id(self):
        self.assertEqual(
            self.response.data.get("created_by").hex, user_id_to_hex(self.user.id)
        )
