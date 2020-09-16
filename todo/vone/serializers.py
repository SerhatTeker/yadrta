from rest_framework import serializers

from vone.models import Category, Tag, Task

base_model_mixin_fields = ["uuid", "created_by", "created_at", "changed_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = base_model_mixin_fields + ["name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = base_model_mixin_fields + ["name"]


class TaskSerializer(serializers.ModelSerializer):
    # Disable due to
    # The `.create()` method does not support writable dotted-source fields by default.
    # -------------------------------------------------------------------------
    # tag = serializers.CharField(source="tag.name")
    # category = serializers.CharField(source="category.name")
    # created_by = serializers.CharField(source="created_by.username")

    class Meta:
        model = Task
        fields = base_model_mixin_fields + [
            "title",
            "description",
            "status",
            "tag",
            "category",
        ]
