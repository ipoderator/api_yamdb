from rest_framework import serializers

from reviews.models import Comment, Review, User


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

    def validate(self, attrs):
        """
        Validate that `author` and `title` pair is not in DB.
        """
        # attrs['author'] = self.context['request'].user
        attrs['author'] = User.objects.get(pk=1)
        attrs['title'] = self.context['request'].parser_context['kwargs'].get(
            'title_id')
        if Review.objects.filter(
            author=attrs['author'],
            title=attrs['title']
        ):
            raise serializers.ValidationError(
                'User can have only one review for a single title.'
            )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment model serializer.

    Include fields:
    * id (read only);
    * text;
    * author (read only) - string username;
    * pub_date (read only).
    """

    author = serializers.SlugField(
        'username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = (
            'pub_date',
        )
