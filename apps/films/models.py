from django.urls import reverse
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Film(models.Model):
    title = models.CharField(verbose_name="Название", max_length=255)
    year = models.PositiveIntegerField(verbose_name="Год", null=True, blank=True)
    poster = models.TextField(verbose_name="Постер в Base64", blank=True)
    kinopoisk_url = models.URLField(verbose_name="URL адрес на Кинопоиск", blank=True)
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка", default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    review = models.TextField(verbose_name="Рецензия")
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    def get_absolute_url(self):
        return reverse('films:film-detail', args=(self.id,))

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["-created"]
