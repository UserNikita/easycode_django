from datetime import timedelta

from django import template
from django.db.models import Count

register = template.Library()


@register.inclusion_tag(filename="youtube/playlist_sidebar.html", takes_context=True)
def include_playlists(context):
    channel = context["channel"]
    context.update({
        'playlists': channel.playlist_set.all().annotate(videos_count=Count("video")),
        'without_playlist_videos_count': channel.video_set.filter(playlist=None).count(),
        'all_videos_count': channel.video_set.count(),
    })
    return context


@register.filter()
def duration(value: int):
    return str(timedelta(seconds=value))
