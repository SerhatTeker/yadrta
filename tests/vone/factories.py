import factory
from faker import Faker

from src.vone.models import Category, Tag, Task
from tests.users.factories import UserFactory

fake = Faker()


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


# Status states for Task model
STATES = ["todo", "wip", "suspended", "waiting", "done"]


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
        django_get_or_create = ("title",)

    id = factory.Faker("pyint")
    created_at = factory.Faker("date")
    changed_at = factory.Faker("date")
    created_by = factory.SubFactory(UserFactory)
    title = factory.Faker("word")
    description = factory.Faker("sentence")
    status = fake.word(ext_word_list=STATES)
    tag = factory.SubFactory(TagFactory)
    category = factory.SubFactory(CategoryFactory)
