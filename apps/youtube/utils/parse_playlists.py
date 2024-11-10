from pytubefix import Channel

from apps.youtube import models


def parse_playlists(channel: models.Channel):
    yt = Channel(channel.url)

    for p in yt.playlists:
        playlist = models.Playlist(
            id=p.playlist_id,
            url=p.playlist_url,
            title=p.title,
            channel=channel,
        )
        playlist.save()
