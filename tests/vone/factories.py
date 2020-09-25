import factory

from src.vone.models import Tag
from tests.users.factories import UserFactory


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ("name",)

    id = factory.Faker("pyint")
    name = factory.Faker("word")
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date")
    changed_at = factory.Faker("date")
