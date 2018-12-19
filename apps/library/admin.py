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


class BookFileInline(admin.StackedInline):
    model = BookFile
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('get_cover', 'title', 'year',)
    list_filter = ('year', 'category', CoverThumbnailFilter, 'publishers', 'authors',)
    filter_horizontal = ('authors', 'publishers', 'tags',)
    inlines = (BookFileInline,)
    form = BookAdminForm


class AuthorAdmin(admin.ModelAdmin):
    pass


class PublisherAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
