from django.urls import path
from .views import *

urlpatterns = [
    path(
        route="channels/",
        view=ChannelsListView.as_view(),
        name='channels-list'
    ),
    path(
        route="channels/<str:channel_pk>/videos/",
        view=VideosListView.as_view(),
        name='videos-list'
    ),
    path(
        route="channels/<str:channel_pk>/playlists/<str:playlist_pk>/videos/",
        view=PlaylistVideosListView.as_view(),
        name='playlist-videos-list'
    ),
    path(
        route="channels/<str:channel_pk>/videos-without-playlist/",
        view=WithoutPlaylistVideosListView.as_view(),
        name='without-playlist-videos-list'
    ),
    path(
        route="channels/add/",
        view=AddChannelFormView.as_view(),
        name='channel-add'
    ),
    path(
        route="videos/<str:pk>/toggle-viewed-status/",
        view=ToggleViewedUpdateView.as_view(),
        name='video-toggle-viewed-status'
    ),
    path(
        route="channels/<str:pk>/update-data/",
        view=UpdateChannelDataUpdateView.as_view(),
        name='update-channel-data'
    )
]
