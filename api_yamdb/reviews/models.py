from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    """
    Review model.

    Fields:
    * text(Text) - review text;
    * author(Int) - FK to Users model, cascade on delete;
    * title(Int) - FK to Title model, cascade on delete;
    * score(Int) - title score, range from 1 to 10;
    * pub_date(DateTime) - review add date, auto on add.

    User can have only one review for a single title.
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
    # title = models.ForeignKey(
    #     Title,
    #     models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Произведение'
    # )
    title = models.IntegerField()
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


class Comment(models.Model):
    """
    Comment model.

    Fields:
    * text(Text) - comment text;
    * author(Int) - FK to Users model, cascade on delete;
    * review(Int) - FK to Review model, cascade on delete;
    * pub_date(DateTime) - review add date, auto on add.

    User can have only one review for a single title.
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
