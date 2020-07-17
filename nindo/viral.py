from .channel import ChannelType
from .util import parse_timestamp


__all__ = (
    "Viral",
    "ViralPost"
)


class Viral:
    __slots__ = (
        "platform",
        "post_id",
        "timestamp",
        "type",
        "value",
        "post"
    )

    def __init__(self, data, http):
        self.platform = ChannelType(data["platform"])
        self.post_id = data["postID"]
        self.timestamp = parse_timestamp(data["timestamp"])
        self.type = data["type"]
        self.value = data["value"]

        self.post = data["_post"]
        if self.post is not None:
            self.post = ViralPost(self.post, http)


class ViralPost:
    __slots__ = (
        "fsk_18",
        "ad",
        "clickbait",
        "content_checked",
        "shitstorm",
        "title",
        "channel_id",
        "artist_id",
        "analytics",
        "_http"
    )

    def __init__(self, data, http):
        self.fsk_18 = data["FSK18"]
        self.ad = data["ad"]
        self.clickbait = data["clickbait"]
        self.content_checked = data["contentChecked"]
        self.shitstorm = data["shitstorm"]
        self.title = data.get("title")

        # I hate this so much lol
        # The api doesn't give us the channel type, so we can't fetch it directly
        self.channel_id = data.get("_channel", {}).get("channelID")
        self.artist_id = data.get("_channel", {}).get("_artist", {}).get("_id")

        self._http = http

    async def get_artist(self):
        from .artist import DetailedArtist
        data = await self._http.request(f"/artist/{self.artist_id}")
        return DetailedArtist(data, http=self._http)
