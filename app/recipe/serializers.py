"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)


# move to top since gonna be nested into recipe
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)  # optional

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

    # by default, nested serializers is read-only, we need to overridden
    # to customize to be able to add tags
    def create(self, validated_data):
        """Create a recipe."""
        # remove tags from validated data if exists
        # if tag doesn't exist, use []
        tags = validated_data.pop('tags', [])
        # Recipe model expects tags to be assigned as a related field,
        # so expects it to be created separately and added as a
        # relationship to recipe from the manytomany field
        recipe = Recipe.objects.create(**validated_data)
        # The context is passed to the sterilizer by the view when
        # you're using the sterilizer for that particular view.
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # name=tag['name'],
                **tag,
            )
            recipe.tags.add(tag_obj)

        return recipe
