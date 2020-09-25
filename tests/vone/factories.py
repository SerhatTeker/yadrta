import factory

from src.vone.models import Category, Tag
from tests.users.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    id = factory.Faker("pyint")
    name = factory.Faker("word")
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date")
    changed_at = factory.Faker("date")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ("name",)

    id = factory.Faker("pyint")
    name = factory.Faker("word")
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date")
    changed_at = factory.Faker("date")
