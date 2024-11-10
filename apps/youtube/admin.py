from django.contrib import admin
from .models import Channel, Playlist, Video
from .utils.parse_playlists import parse_playlists
from .utils.parse_videos import parse_videos


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ["title", "url"]
    actions = ["parse_playlists", "parse_videos"]

    def parse_playlists(self, request, queryset):
        for channel in queryset:
            parse_playlists(channel=channel)

    parse_playlists.short_description = "Получить плейлисты"

    def parse_videos(self, request, queryset):
        for channel in queryset:
            parse_videos(channel=channel)

    parse_videos.short_description = "Получить видеоролики"


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "channel"]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "publish_date"]
