from datetime import timedelta

from django.urls import reverse
from django.db import models


class Channel(models.Model):
    id = models.CharField(verbose_name="Id", max_length=255, primary_key=True)
    url = models.URLField(verbose_name="Url", unique=True, help_text="URL адрес главной страницы канала")
    title = models.CharField(verbose_name="Название", max_length=255)
    thumbnail_url = models.URLField(verbose_name="Ссылка на превью", blank=True)
    last_update = models.DateTimeField(verbose_name="Дата последнего обновления", null=True)

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("youtube:videos-list", kwargs={"channel_pk": self.pk})

    def video_duration_sum(self):
        return self.video_set.all().aggregate(total_duration=models.Sum("duration"))["total_duration"]


class Playlist(models.Model):
    id = models.CharField(verbose_name="Id", max_length=255, primary_key=True)
    url = models.URLField(verbose_name="Url", unique=True)
    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True)
    channel = models.ForeignKey(verbose_name="Канал", to="Channel", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("youtube:playlist-videos-list", kwargs={"channel_pk": self.channel_id, "playlist_pk": self.pk})


class Video(models.Model):
    id = models.CharField(verbose_name="Id", max_length=255, primary_key=True)
    url = models.URLField(verbose_name="Url", unique=True)
    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True)
    duration = models.PositiveIntegerField(verbose_name="Продолжительность", default=0, help_text="В секундах")
    thumbnail_url = models.URLField(verbose_name="Ссылка на превью", blank=True)
    publish_date = models.DateTimeField(verbose_name="Дата публикации")
    channel = models.ForeignKey(verbose_name="Канал", to="Channel", on_delete=models.CASCADE)
    playlist = models.ForeignKey(
        verbose_name="Плейлист", to="Playlist", on_delete=models.SET_NULL, null=True, blank=True
    )
    viewed = models.ManyToManyField(
        verbose_name="Просмотрено", to="personal_area.Profile", blank=True, through="VideoView"
    )

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["-publish_date"]

    def __str__(self):
        return self.title

    def duration_display(self):
        return str(timedelta(seconds=self.duration))

    def toggle_viewed_url(self):
        return reverse("youtube:video-toggle-viewed-status", kwargs={"pk": self.pk})


class VideoView(models.Model):
    profile = models.ForeignKey(verbose_name="Пользователь", to="personal_area.Profile", on_delete=models.CASCADE)
    video = models.ForeignKey(verbose_name="Пользователь", to="Video", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Время просмотра", auto_now=True)

    class Meta:
        verbose_name = "Просмотр видео"
        verbose_name_plural = "Просмотры видео"
