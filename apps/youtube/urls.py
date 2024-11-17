from django.urls import path
from .views import *

urlpatterns = [
    path(
        route="channels/",
        view=ChannelsListView.as_view(),
        name='channels-list'
    ),
    path(
        route="channels/<str:pk>/videos/",
        view=VideosListView.as_view(),
        name='videos-list'
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
