import logging

from django.forms.models import model_to_dict
from rest_framework.test import APITestCase

from src.vone.serializers import CategorySerializer, TagSerializer, TaskSerializer
from tests.users.factories import UserFactory
from tests.vone.factories import CategoryFactory, TagFactory, TaskFactory

LOGGER = logging.getLogger(__name__)


class UpdateModelDataMixin:
    def update_model_data(self):
        self.user = UserFactory()
        self.tag = TagFactory()
        self.category = CategoryFactory()
        self.model_data = model_to_dict(self.factory_class.build())
        self.model_data.update(
            {
                "created_by": self.user.id,
                "tag": self.tag.id,
                "category": self.category.id,
            }
        )


class BaseTestSerializers(UpdateModelDataMixin, APITestCase):
    pass


class TestCategorySerializer(BaseTestSerializers):
    def setUp(self):
        self.serializer_class = CategorySerializer
        self.factory_class = CategoryFactory
        self.update_model_data()

    def test_serializer_with_empty_data(self):
        serializer = self.serializer_class(data={})
        self.assertEqual(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = self.serializer_class(data=self.model_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_name_field(self):
        serializer = self.serializer_class(data=self.model_data)
        self.assertEqual(serializer.is_valid(), True)

        category = serializer.save()
        self.assertEqual(self.model_data.get("name"), category.name)


class TestTagSerializer(BaseTestSerializers):
    def setUp(self):
        self.serializer_class = TagSerializer
        self.factory_class = TagFactory
        self.update_model_data()

    def test_serializer_with_empty_data(self):
        serializer = self.serializer_class(data={})
        self.assertEqual(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = self.serializer_class(data=self.model_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_name_field(self):
        serializer = self.serializer_class(data=self.model_data)
        self.assertEqual(serializer.is_valid(), True)

        tag = serializer.save()
        self.assertEqual(self.model_data.get("name"), tag.name)


class TestTaskSerializer(BaseTestSerializers):
    def setUp(self):
        self.serializer_class = TaskSerializer
        self.factory_class = TaskFactory
        self.update_model_data()

    def test_serializer_with_empty_data(self):
        serializer = self.serializer_class(data={})
        self.assertEqual(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = self.serializer_class(data=self.model_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_name_field(self):
        serializer = self.serializer_class(data=self.model_data)
        self.assertEqual(serializer.is_valid(), True)

        task = serializer.save()
        self.assertEqual(self.model_data.get("title"), task.title)
