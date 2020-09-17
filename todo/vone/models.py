from django.db import models

from todo.core.utils.models import BaseModelMixin


class Category(BaseModelMixin):
    name = models.CharField(max_length=200, blank=False, verbose_name="Category Name")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(BaseModelMixin):
    name = models.CharField(max_length=200, blank=False, verbose_name="Tag Name")

    def __str__(self):
        return self.name


class Task(BaseModelMixin):
    STATES = (
        ("todo", "Todo"),
        ("wip", "Work in Progress"),
        ("suspended", "Suspended"),
        ("waiting", "Waiting"),
        ("done", "Done"),
    )

    title = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATES, default="todo")
    tag = models.ForeignKey(to=Tag, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.created_by}:{self.title}"
