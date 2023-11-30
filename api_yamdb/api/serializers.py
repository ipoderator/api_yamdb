from rest_framework import serializers

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
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
        """Validate that `author` and `title` pair is not in DB."""
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title = self.context['request'].parser_context.get(
                'kwargs').get('title_id')
            if Review.objects.filter(
                author=author,
                title=title
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
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализотор для возврата списка произвдений."""

    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(
        read_only=True
    )
    rating = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def to_representation(self, instance):
        return TitleGetSerializer().to_representation(instance)

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            return Title.objects.create(**validated_data)
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.create(
                genre_id=genre,
                title_id=title
            )
        return title


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
