from django import template
from django.db.models import Count

register = template.Library()


@register.inclusion_tag(filename="youtube/playlist_sidebar.html", takes_context=True)
def include_playlists(context):
    context.update({
        'playlists': context["channel"].playlist_set.all().annotate(videos_count=Count("video")),
    })
    return context
