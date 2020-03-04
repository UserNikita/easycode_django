from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from .forms import PostFormAdmin
from .models import *
from apps.personal_area.models import Like


class CategoryAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


class LikeInline(GenericStackedInline):
    model = Like
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category',)
    list_filter = ('category', 'author', 'create_date', 'change_date',)
    filter_horizontal = ('tags',)
    readonly_fields = ('create_date', 'change_date',)
    form = PostFormAdmin
    inlines = [LikeInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'create_date',)
    readonly_fields = ('create_date',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
