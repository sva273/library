from django.core.exceptions import ValidationError
from . import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    date_of_birth = models.DateField(verbose_name='Дата рождения', validators=[validate_is_adult])
    profile = models.URLField(null=True, blank=True, verbose_name='Ссылка на профиль')
    is_deleted = models.BooleanField(default=False, verbose_name='Удален ли автор', help_text='Если False - автор активен. Если True - автора больше нет в списке доступных')
    rating = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name='Рейтинг автора')

    def __str__(self):
        return f'{self.first_name} {self.last_name}  ({self.date_of_birth})'

class AuthorDetail(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='details')
    biography = models.TextField()
    birth_city = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=Gender.choices)

    def __str__(self):
        return f"{self.author} by {self.birth_city}"


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Категория', unique=True)

    def __str__(self):
        return self.name


class Library(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название библиотеки')
    location = models.CharField(max_length=100, verbose_name='Локация')
    site = models.URLField(verbose_name='Сайт')

    def __str__(self):
        return f"{self.title} by ({self.location})"


class Member(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    gender = models.CharField(max_length=10, choices=Gender.choices, verbose_name='Пол')
    date_of_birth = models.DateField(validators=[validate_age])

    role = models.CharField(max_length=20, choices=Role.choices, verbose_name='Роль', default=Role.STAFF)
    is_active = models.BooleanField(default=True)
    libraries = models.ManyToManyField(Library,related_name='members')

    @property
    def age(self):
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def __str__(self):
        return f"{self.first_name} by {self.last_name} by ({self.role})"


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название книги')
    author = models.ForeignKey(Author,max_length=100, on_delete=models.PROTECT, verbose_name='Автор')
    publishing_date = models.DateField(verbose_name='Дата публикации', validators=[validate_published_date])
    summary = models.TextField(verbose_name='Краткое описание', null=True, blank=True)
    page_count = models.SmallIntegerField(verbose_name='Количество страниц', null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5000)])
    genre = models.CharField(max_length=100, verbose_name='Жанр', null=True, blank=True, choices=Genre.choices)
    publisher = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, related_name='books')
    libraries = models.ManyToManyField(Library, related_name='books')

    def __str__(self):
        return f"{self.title} by {self.author} by {self.publishing_date}"

    @property
    def rating(self):
        return  self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0


class Post(models.Model):
    title = models.CharField(max_length=255, unique_for_date='created_at',verbose_name='Название')
    body = models.TextField(verbose_name='Текст поста')
    author = models.ForeignKey(Member, on_delete=models.CASCADE,  related_name='posts')
    is_moderated = models.BooleanField(default=False, verbose_name='Промодерировано')
    library = models.ForeignKey(Library, on_delete=models.CASCADE,  related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.title


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='borrows')
    borrow_date = models.DateField(auto_now_add=True, verbose_name='Дата взятия книги')
    return_date = models.DateField(verbose_name='Дата возврата')
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book} by {self.member}"

    def is_overdue(self):
        if self.is_returned:
            return False
        return self.return_date < timezone.now().date()

    def clean(self):
        super().clean()
        if self.borrow_date and self.return_date and self.borrow_date > self.return_date:
            raise ValidationError('Дата возврата книги не может быть позже даты взятия')


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f"{self.book} by {self.reviewer}"
