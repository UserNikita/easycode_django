from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'changed',)
    readonly_fields = ('created', 'changed',)


admin.site.register(Note, NoteAdmin)
