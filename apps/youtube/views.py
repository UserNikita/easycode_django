from datetime import timedelta

from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Prefetch, Exists, OuterRef, Sum

from apps.youtube.models import Channel, Video, VideoView, Playlist
from apps.youtube.forms import ChannelForm
from apps.youtube.utils.update_channel_data import update_channel


class ChannelsListView(LoginRequiredMixin, ListView):
    template_name = "youtube/list_channels.html"
    queryset = Channel.objects.all()


class VideosListView(LoginRequiredMixin, ListView):
    template_name = "youtube/list_videos.html"
    context_object_name = "video_list"
    model = Video

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(channel__pk=self.kwargs["channel_pk"])
        if "playlist_pk" in self.kwargs:
            qs = qs.filter(playlist__pk=self.kwargs["playlist_pk"])
        qs = qs.select_related("playlist")
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
        channel = Channel.objects.get(pk=self.kwargs["channel_pk"])
        context["channel"] = channel
        if self.kwargs.get("playlist_pk"):
            context["current_playlist"] = Playlist.objects.get(pk=self.kwargs["playlist_pk"])

        qs = context["object_list"]
        all_duration = qs.aggregate(duration=Sum("duration"))["duration"]
        viewed = qs.exclude(viewed=None).aggregate(duration=Sum("duration"))["duration"]
        not_viewed = qs.filter(viewed=None).aggregate(duration=Sum("duration"))["duration"]

        context["duration"] = {
            "all": str(timedelta(seconds=all_duration)) if all_duration else "Нет видео",
            "viewed": str(timedelta(seconds=viewed)) if viewed else "Нет просмотренных видео",
            "not_viewed": str(timedelta(seconds=not_viewed)) if not_viewed else "Нет непросмотренных видео",
            "progress": 100 / all_duration * (viewed or 0) if all_duration else 0  # Процент просмотренного
        }
        return context


class PlaylistVideosListView(VideosListView):
    pass


class WithoutPlaylistVideosListView(VideosListView):
    def get_queryset(self):
        return super().get_queryset().filter(playlist=None)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["without_playlist"] = True
        return context


class ToggleViewedUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    fields = []

    def get_success_url(self):
        return self.object.channel.get_absolute_url()

    def get_object(self, queryset=None):
        video = super().get_object()
        if video_view := VideoView.objects.filter(video=video, profile=self.request.user.profile).first():
            video_view.delete()
        else:
            VideoView.objects.create(profile=self.request.user.profile, video=video)
        return video


class AddChannelFormView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "youtube/add_channel.html"
    form_class = ChannelForm

    def test_func(self):
        return self.request.user.is_staff


class UpdateChannelDataUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Channel
    fields = []

    def test_func(self):
        return self.request.user.is_staff

    def get_object(self, queryset=None):
        channel = super().get_object(queryset=queryset)
        update_channel(channel=channel)
        channel.last_update = now()
        channel.save()
        return channel
