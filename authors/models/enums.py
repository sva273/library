from django.db import models

class Genre(models.TextChoices):
    FICTION = 'Fiction', 'Fiction'
    NON_FICTION = 'Non-Fiction', 'Non-Fiction'
    SCIENCE = 'Science Fiction', 'Science'
    FANTASY = 'Fantasy', 'Fantasy'
    MYSTERY = 'Mystery', 'Mystery'
    BIOGRAPHY = 'Biography', 'Biography'


class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHERS = 'other', 'Other'


class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    STAFF = 'staff', 'Staff'
    READER = 'reader', 'Reader'