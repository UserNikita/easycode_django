from pytubefix import Channel as BaseChannel, Playlist

from apps.youtube import models


class Channel(BaseChannel):
    """Класс для исправления проблемы связанной с изменением ключей в словаре."""

    def _extract_playlist_id(self, x: dict):
        x["gridPlaylistRenderer"] = x.pop("lockupViewModel")
        x["gridPlaylistRenderer"]["playlistId"] = x["gridPlaylistRenderer"].pop("contentId")
        return super()._extract_playlist_id(x)


def update_channel(channel: models.Channel):
    update_playlists(channel=channel)
    for p in channel.playlist_set.all():
        update_videos_in_playlist(playlist=p)
    update_videos(channel=channel)


def update_playlists(channel: models.Channel):
    c = Channel(channel.url)

    for p in c.playlists:
        if channel.playlist_set.filter(pk=p.playlist_id).exists():
            continue
        try:
            models.Playlist.objects.create(
                id=p.playlist_id,
                url=p.playlist_url,
                title=p.title,
                channel=channel,
            )
        except:
            print(p.title)


def update_videos_in_playlist(playlist: models.Playlist):
    for v in Playlist(url=playlist.url).videos:
        if video := models.Video.objects.filter(id=v.video_id).first():
            video.playlist = playlist
            video.save()
        else:
            try:
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
            except:
                print(v.title)


def update_videos(channel: models.Channel):
    for v in Channel(channel.url).videos:
        if models.Video.objects.filter(pk=v.video_id).exists():
            continue
        try:
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
        except:
            print(v.title)
