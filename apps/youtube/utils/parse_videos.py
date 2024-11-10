from pytubefix import Channel

from apps.youtube import models


def parse_videos(channel: models.Channel):
    yt = Channel(channel.url)

    for v in yt.videos:
        video = models.Video(
            id=v.video_id,
            url=v.watch_url,
            title=v.title,
            description=v.description.encode("utf-8"),  # TODO: Поправить баг с юникодом
            duration=v.length,
            thumbnail_url=v.thumbnail_url,
            publish_date=v.publish_date,
            channel=channel,
            # playlist =
        )
        try:
            video.save()
        except:
            pass
