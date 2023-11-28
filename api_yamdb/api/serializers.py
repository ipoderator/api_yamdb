from rest_framework import serializers

from reviews.models import (
    Category,
    Comment,
    Genre,
    Title,
    Review,
)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review model serializer.

    Include fields:
    * id (read only);
    * text;
    * author (read only) - string username;
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
            'score',
            'pub_date',
        )
        read_only_fields = (
            'pub_date',
        )

    def validate(self, attrs):
        """
        Validate that `author` and `title` pair is not in DB.
        """
        if self.context['request'].method == 'POST':
            attrs['author'] = self.context['request'].user
            attrs['title'] = self.context['request'].parser_context.get(
                'kwargs').get('title_id')
            if Review.objects.filter(
                author=attrs['author'],
                title=attrs['title']
            ):
                raise serializers.ValidationError(
                    'User can have only one review for a single title.'
                )
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализотор для возврата списка произвдений."""    

    genre = GenreSerializer(
        many = True,
        read_only = True
    )
    category = CategorySerializer(
        read_only = True
    )
    reting = serializers.IntegerField(
        read_only = True,
        default = 0
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='genre',
        queryset=Genre.objects.all(),
        many = True
    )
    category = serializers.SlugRelatedField(
        slug_field='category',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__' 

    def to_representation(self, instance):
        return TitleGetSerializer().to_representation(instance)


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
    fields = (
        'id',
        'text',
        'author',
        'pub_date',
    )
    read_only_fields = (
        'pub_date',
    )
