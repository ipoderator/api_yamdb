from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
    GenreTitle, 
    User
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'role',)
    search_fields = ('username', 'role',)
    list_editable = ('role',)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-empty-'


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    """Админка жанров"""
    list_display = (
        'pk', 
        'name', 
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    """Админка произведений"""
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre',)
    empty_value_display = '-empty-'
    list_editable = ('category',)
    exclude = ('genre',)


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    """Админка отзывов"""
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('title', 'author', 'pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    """Админка сомментариев"""
    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review', 'author', 'pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'
    


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    """Админка прозведений и жанров"""
    list_display = (
        'pk',
        'genre',
        'title',
    )
    search_fields = ('title',)
    list_filter = ('genre',)
    empty_value_display = '-empty-'


