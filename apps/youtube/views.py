from django.views.generic import ListView
from apps.youtube.models import Channel, Video


class ChannelsListView(ListView):
    template_name = "youtube/list_channels.html"
    queryset = Channel.objects.all()


class VideosListView(ListView):
    template_name = "youtube/list_videos.html"
    context_object_name = "video_list"
    queryset = Video.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["channel"] = Channel.objects.get(pk=self.kwargs["pk"])
        return context