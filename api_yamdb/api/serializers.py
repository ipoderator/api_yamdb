from rest_framework import serializers

from reviews.models import (
    Category, 
    Genre, 
    Title, 
    Review,
    Comment,
)


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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзывов."""

    author = serializers.StringRelatedField(
        slug_field='username',
        read_only = True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        read_only = ('id',) 



class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only = True,
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only = ('review',)