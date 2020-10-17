from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict
from rest_framework.test import APITestCase
from src.users.serializers import CreateUserSerializer
from tests.users.factories import UserFactory


class TestCreateUserSerializer(APITestCase):
    def setUp(self):
        self.user_data = model_to_dict(UserFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = CreateUserSerializer(data={})
        self.assertEqual(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = CreateUserSerializer(data=self.user_data)
        self.assertEqual(serializer.is_valid(), True)

    def test_serializer_hashes_password(self):
        serializer = CreateUserSerializer(data=self.user_data)
        self.assertEqual(serializer.is_valid(), True)

        user = serializer.save()
        self.assertEqual(
            check_password(self.user_data.get("password"), user.password), True
        )
