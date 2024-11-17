from pytubefix import YouTube, Playlist, Channel as BaseChannel

# yt = YouTube("http://youtube.com/watch?v=1PzL6jrBaYY")
# print(yt.title)

# pl = Playlist("https://www.youtube.com/playlist?list=PLhZj4EWV4TnhbH8teW8unmUAZB9BQIpht")
#
# print("Название плейлиста:", pl.title)
#
# for v in pl.videos:
#     print()
#     print(v.channel_url)
#     print("Название видео:", v.title)
#     # print("Описание:", v.description)
#     # print("Просмотров:", v.views)
#     print("Ссылка на обложку:", v.thumbnail_url)
#     print("Дата публикации:", v.publish_date)
#     print("Продолжительность:", f"{v.length/60} min {v.length%60} sec")
#     break


class Channel(BaseChannel):
    def _extract_playlist_id(self, x: dict):
        print(x)
        x["gridPlaylistRenderer"] = x.pop("lockupViewModel")
        x["gridPlaylistRenderer"]["playlistId"] = x["gridPlaylistRenderer"].pop("contentId")
        return super()._extract_playlist_id(x)


c = Channel(url="https://www.youtube.com/@t0digital")

data = c.initial_data["contents"]

print(c.playlists)

print()
# p = Playlist("https://www.youtube.com/playlist?list=PLAk6CfuV7hyp2TEcPKSW1fZFXsfLmky6x")
#
# print(p.video_urls)
