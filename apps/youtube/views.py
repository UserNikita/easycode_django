from django.views.generic import ListView, CreateView
from apps.youtube.models import Channel, Video
from apps.youtube.forms import ChannelForm


class ChannelsListView(ListView):
    template_name = "youtube/list_channels.html"
    queryset = Channel.objects.all()


class VideosListView(ListView):
    template_name = "youtube/list_videos.html"
    context_object_name = "video_list"
    model = Video

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(channel__pk=self.kwargs["pk"]).select_related("playlist")
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["channel"] = Channel.objects.get(pk=self.kwargs["pk"])
        return context


class AddChannelFormView(CreateView):
    template_name = "youtube/add_channel.html"
    form_class = ChannelForm
