from django.contrib import admin
from .models import *
from .forms import BookAdminForm


class BookFileInline(admin.StackedInline):
    model = BookFile
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('get_cover', 'title', 'year',)
    list_filter = ('year', 'category', 'publishers', 'authors',)
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
