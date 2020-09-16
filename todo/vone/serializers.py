from rest_framework import serializers

from vone.models import Category, Tag, Task

base_model_mixin_fields = ["uuid", "created_by", "created_at", "changed_at"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = base_model_mixin_fields + [
            "title",
            "description",
            "status",
            "tag",
            "category",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = base_model_mixin_fields + ["name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = base_model_mixin_fields + ["name"]
