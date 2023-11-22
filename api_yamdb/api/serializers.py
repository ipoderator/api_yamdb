from rest_framework import serializers

from reviews.models import Review
from rest_framework.validators import UniqueTogetherValidator


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review model serializer.

    Include fields:
    * id (read only);
    * text;
    * author (read only) - string username;
    * title (read only);
    * score;
    * pub_date (read only).
    """

    author = serializers.SlugField(
        'username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'title',
            'score',
            'pub_date',
        )
        read_only_fields = (
            'pub_date',
            'title',
        )
        validators = [
            UniqueTogetherValidator(
                Review,
                ('author', 'title')
            )
        ]
