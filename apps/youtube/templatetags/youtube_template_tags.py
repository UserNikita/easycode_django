from django import template

register = template.Library()


@register.inclusion_tag(filename="youtube/playlist_sidebar.html", takes_context=True)
def include_playlists(context):
    context.update({
        'playlists': context["channel"].playlist_set.all(),
    })
    return context
