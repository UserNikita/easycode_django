from django import forms
from pytubefix import Channel as YTChannel

from .models import Channel


class ChannelForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        channel = YTChannel(url=instance.url)
        instance.pk = channel.channel_id
        instance.title = channel.channel_name
        instance.thumbnail_url = channel.thumbnail_url
        instance.save()
        return instance

    class Meta:
        model = Channel
        fields = ["url"]
