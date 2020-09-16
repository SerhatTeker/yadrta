from rest_framework import serializers

from vone.models import Category, Tag, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "tag",
            "category",
            # BaseModelMixin
            "id",
            "created_at",
            "changed_at",
            "created_by",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            # BaseModelMixin
            "id",
            "created_at",
            "changed_at",
            "created_by",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
            # BaseModelMixin
            "id",
            "created_at",
            "changed_at",
            "created_by",
        )
