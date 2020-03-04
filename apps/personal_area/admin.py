from django.contrib import admin
from .models import *


class LikeAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'content_type', 'creation_date',)
    list_filter = ('user', 'content_type', 'creation_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'author', 'content_type', 'creation_date')
    list_filter = ('author', 'content_type', 'creation_date',)


admin.site.register(Profile)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
