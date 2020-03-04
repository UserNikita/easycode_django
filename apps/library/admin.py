from django.contrib import admin
from .models import *
from .forms import BookAdminForm


class CoverThumbnailFilter(admin.SimpleListFilter):
    """
    Класс для фильтрации книг в админке по наличию миниатюры для обложки
    """
    title = "Миниатюрная обложка"
    parameter_name = 'cover_thumbnail'

    def lookups(self, request, model_admin):
        return ('no', "Нет"), ('yes', "Есть")

    def queryset(self, request, queryset):
        if self.value() == 'no':
            return queryset.filter(cover_thumbnail='')
        elif self.value() == 'yes':
            return queryset.exclude(cover_thumbnail='')
        return queryset


class BookAdmin(admin.ModelAdmin):
    list_display = ('get_cover', 'title', 'year',)
    list_filter = ('year', CoverThumbnailFilter, 'publishers', 'authors',)
    filter_horizontal = ('authors', 'publishers', 'tags',)
    actions = ('create_cover_thumbnails',)
    form = BookAdminForm

    def create_cover_thumbnails(self, request, queryset):
        for book in queryset.filter(cover_thumbnail=''):
            book.save()  # После сохранения сгенерируется миниатюрная обложка
    create_cover_thumbnails.short_description = 'Создать миниатюрные обложки'


class AuthorAdmin(admin.ModelAdmin):
    pass


class PublisherAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Tag, TagAdmin)
