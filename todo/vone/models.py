import uuid

from django.conf import settings
from django.db import models

USER = settings.AUTH_USER_MODEL


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `changed_at` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreatedbyModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_by` field.
    """

    created_by = models.ForeignKey(
        to=USER,
        # related_name="todos",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    An abstract base class model that provides id field,
    using uuid4.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Category(UUIDModel, CreatedbyModel, TimeStampedModel):
    name = models.CharField(max_length=200, blank=False, verbose_name="Category Name")

    def __str__(self):
        return self.name


class Tag(UUIDModel, CreatedbyModel, TimeStampedModel):
    name = models.CharField(max_length=200, blank=False, verbose_name="Tag Name")

    def __str__(self):
        return self.name


class Task(UUIDModel, CreatedbyModel, TimeStampedModel):
    STATES = (
        ("todo", "Todo"),
        ("wip", "Work in Progress"),
        ("suspended", "Suspended"),
        ("waiting", "Waiting"),
        ("done", "Done")
    )

    title = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=4, choices=STATES, default="todo")
    tag = models.ForeignKey(to=Tag, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.title}_{self.created_by}"
