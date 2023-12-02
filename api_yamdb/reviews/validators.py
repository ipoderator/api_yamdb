from django.core.exceptions import ValidationError
from django.utils import timezone


def now_year_validator(year):
    """Functions to check the year."""
    if year > timezone.now().year:
        raise ValidationError(
            f"Вы не можете использовать этот год - {year}",
            code='invalid',
            params={'year': year},
        )
