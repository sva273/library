from django.contrib import admin
from .models.books import Author, Book, Category, Library, Member, Post, Borrow, Review, AuthorDetail
from .models.events import Event, EventParticipant


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    verbose_name = "Author"
    verbose_name_plural = "Authors"
    list_display = ('first_name', 'last_name', 'date_of_birth', 'profile', 'is_deleted', 'rating')
    list_editable = ('is_deleted', 'rating')
    list_filter = ('is_deleted', 'rating')
    search_fields = ('first_name', 'last_name')
    list_per_page = 10
    ordering = ['-rating']




# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Library)
admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Borrow)
admin.site.register(Review)
admin.site.register(AuthorDetail)
admin.site.register(EventParticipant)
admin.site.register(Event)
