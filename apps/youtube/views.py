from datetime import timedelta

from django.views.generic import ListView, CreateView
from django.db.models import Prefetch, Exists, OuterRef, Sum
from apps.youtube.models import Channel, Video, VideoView
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
        # Добавить оптимизацию для поля viewed и оставить в нём только просмотры текущего пользователя
        qs = qs.prefetch_related(
            Prefetch("viewed", queryset=VideoView.objects.filter(profile=self.request.user.profile))
        )
        # Пометить просмотренные данным пользователем видео. Поле is_viewed будет принимать значения True или False
        # qs = qs.annotate(is_viewed=Exists(
        #     VideoView.objects.filter(profile=self.request.user.profile).filter(video=OuterRef("pk")))
        # )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        channel = Channel.objects.get(pk=self.kwargs["pk"])
        context["channel"] = channel

        qs = context["object_list"]
        all_duration = channel.video_duration_sum()
        viewed = qs.exclude(viewed=None).aggregate(duration=Sum("duration"))["duration"]
        not_viewed = qs.filter(viewed=None).aggregate(duration=Sum("duration"))["duration"]

        context["duration"] = {
            "all": str(timedelta(seconds=all_duration)) if all_duration else "Нет видео",
            "viewed": str(timedelta(seconds=viewed)) if viewed else "Нет видео",
            "not_viewed": str(timedelta(seconds=not_viewed)) if not_viewed else "Нет видео",
            "progress": 100 / all_duration * viewed  # Процент просмотренного
        }
        return context


class AddChannelFormView(CreateView):
    template_name = "youtube/add_channel.html"
    form_class = ChannelForm
