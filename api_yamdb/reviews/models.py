from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.constraints import UniqueConstraint

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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    author  = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        validators=[
            MinValueValidator(
            1,
            message='Вы ввели слишком низкую оценку!'
        ),
            MaxValueValidator(
            10,
            message='Вы ввели слишком высокую оценку!'
        ),   
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now=True,
        db_index=True
    )

    class Meta:
        """Проверка на уникальность произведений"""
        constraints = (
            UniqueConstraint(
                fields=('title', 'author'),
                name='title_and_author_unique',
            ),
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:LENGTH_CHAR]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='отзыв',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now=True,
        db_index=True
    )


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


    def __str__(self):
        return self.text[:LENGTH_CHAR]


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
    