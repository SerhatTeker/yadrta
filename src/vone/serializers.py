from rest_framework import serializers

from src.core.utils.permissions import IsOwnerOrReadOnly
from src.vone.models import Category, Tag, Task

base_model_mixin_fields = ["uuid", "created_by", "created_at", "changed_at"]


class CategorySerializer(serializers.ModelSerializer):
    permission_classes = IsOwnerOrReadOnly

    class Meta:
        model = Category
        fields = ["name", "pk"] + base_model_mixin_fields


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "pk"] + base_model_mixin_fields


class TaskSerializer(serializers.ModelSerializer):
    # Disable due to
    # The `.create()` method does not support writable dotted-source fields by default.
    # -------------------------------------------------------------------------
    # tag = serializers.CharField(source="tag.name")
    # category = serializers.CharField(source="category.name")
    # created_by = serializers.CharField(source="created_by.username")

    class Meta:
        model = Task
        fields = [
            "pk",
            "title",
            "description",
            "status",
            "tag",
            "category",
        ] + base_model_mixin_fields
        # nested representations
        # https://www.django-rest-framework.org/api-guide/serializers/#specifying-nested-serialization
        # depth = 1
