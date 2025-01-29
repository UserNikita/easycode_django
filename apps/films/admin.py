from django.contrib import admin

from apps.films.models import Film


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    pass
