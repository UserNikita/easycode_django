from django.urls import path
from .views import *

urlpatterns = [
    path(
        route="channels/",
        view=ChannelsListView.as_view(),
        name='channels_list'
    ),
    path(
        route="videos/<str:pk>/",
        view=VideosListView.as_view(),
        name='videos-list'
    )
]
