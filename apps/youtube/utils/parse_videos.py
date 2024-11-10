from pytubefix import Channel, Playlist

from apps.youtube import models


def parse_videos(channel: models.Channel):
    for v in Channel(channel.url).videos:
        if models.Video.objects.filter(pk=v.video_id).exists():
            continue
        models.Video.objects.create(
            id=v.video_id,
            url=v.watch_url,
            title=v.title,
            description=v.description.encode("utf-8"),  # TODO: Поправить баг с юникодом
            duration=v.length,
            thumbnail_url=v.thumbnail_url,
            publish_date=v.publish_date,
            channel=channel,
        )


def parse_videos_in_playlist(playlist: models.Playlist):
    for v in Playlist(url=playlist.url).videos:
        if video := models.Video.objects.filter(id=v.video_id).first():
            video.playlist = playlist
            video.save()
        else:
            models.Video.objects.create(
                id=v.video_id,
                url=v.watch_url,
                title=v.title,
                description=v.description.encode("utf-8"),  # TODO: Поправить баг с юникодом
                duration=v.length,
                thumbnail_url=v.thumbnail_url,
                publish_date=v.publish_date,
                channel=playlist.channel,
                playlist=playlist,
            )
