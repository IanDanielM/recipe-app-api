"""Serializers for Recipe API"""

from rest_framework import serializers
from core.models import Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe"""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """serializer for Recipe Detail View"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """seerializer for tags"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
