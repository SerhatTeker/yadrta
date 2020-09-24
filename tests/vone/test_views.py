import factory
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from tests.users.factories import TagFactory, UserFactory

fake = Faker()


# Tag
# ------------------------------------------------------------------------------


class TestTagCreateAPIView(APITestCase):
    """
    Tests /tag create operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("tag-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def test_create_tag(self):
        payload = {"name": "newthing", "created_by": self.user.pk}
        response = self.client.post(self.url, payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class TestTagListView(APITestCase):
    """
    Tests /tag list operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("tag-list")
        self.tag_data = factory.build(dict, FACTORY_CLASS=TagFactory)
        print(f"tag_data: {self.tag_data}")
        print(f"created_by: {self.tag_data['created_by']}")

    def test_get_tag_list_with_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_tag_list_with_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
