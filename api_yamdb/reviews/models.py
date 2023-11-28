from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import now_year_validator

User = get_user_model()

LENGTH_CHAR = 16


class Category(models.Model):
    name = models.CharField(
        verbose_name='Назване категории',
        max_length=100,
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name[:LENGTH_CHAR]


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=100
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LENGTH_CHAR]
    

class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=100
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Дата выхода',
        validators=[now_year_validator],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name= 'Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:LENGTH_CHAR]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение и жанры'
        verbose_name_plural = 'Произведения и жанры'
    
    def __str__(self):
        return f'{self.title}, {self.genre}'


class Review(models.Model):
    """
    Review model.

    Fields:
    * text(Text) - review text;
    * author(Int) - FK to Users model, cascade on delete;
    * title(Int) - FK to Title model, cascade on delete;
    * score(Int) - title score, range from 1 to 10;
    * pub_date(DateTime) - review add date, auto on add.

    User can have only one review for a single title. Ordered by `pub_date`.
    """

    SCORE_ERROR_MESSAGE = 'Score must be in range from 1 to 10'
    text = models.TextField(
        'Текст'
    )
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, SCORE_ERROR_MESSAGE),
            MaxValueValidator(10, SCORE_ERROR_MESSAGE),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]
        ordering = (
            '-pub_date',
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:LENGTH_CHAR]


class Comment(models.Model):
    """
    Comment model.

    Fields:
    * text(Text) - comment text;
    * author(Int) - FK to Users model, cascade on delete;
    * review(Int) - FK to Review model, cascade on delete;
    * pub_date(DateTime) - review add date, auto on add.

    Ordered by `pub_date`.
    """

    text = models.TextField(
        'Текст'
    )
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = (
            '-pub_date',
        )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LENGTH_CHAR]
