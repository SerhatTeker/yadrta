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

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModelMixin(UUIDModel, CreatedbyModel, TimeStampedModel):
    """
    Base Data Model Mixin for data models:
    `created_at`, `changed_at`, `created_by`, `id` which using uuid4.
    """

    class Meta:
        abstract = True
