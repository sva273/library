from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_age(value, min_age=6, max_age=120):
    """Валидация совершеннолетия"""
    today = timezone.now().date()
    if value > today:
        raise ValidationError("Date of birth must be before today")

    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < min_age:
        raise ValidationError(f"You are young than {min_age} years old")

    if age > max_age:
        raise ValidationError(f"You are young than {max_age} years old")


def validate_is_adult(value):
    today = timezone.now().date()
    if value > today:
        raise ValidationError("Date of birth must be before today")

    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError(f"You are young than 18 years old")


def validate_published_date(value):
    """В"""
    today = timezone.now().date()
    if value > today:
        raise ValidationError("Date of published date must be before today")
