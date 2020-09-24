import factory

from src.vone.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    id = factory.Faker("uuid4")
    name = factory.Faker("word")
    created_by = factory.Faker("uuid4")
    created_at = factory.Faker("date")
    changed_at = factory.Faker("date")
