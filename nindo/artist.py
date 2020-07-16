from .channel import Channel, ChannelType

__all__ = (
    "Artist",
    "DetailedArtist",
    "RankedArtist"
)


class Artist:
    __slots__ = (
        "id",
        "name",
        "avatar_url",
        "_http"
    )

    def __init__(self, data, http):
        self.id = data.get("artistID", data["id"])
        self.name = data.get("artistName", data["name"])
        self.avatar_url = data["avatar"]

        self._http = http


class DetailedArtist(Artist):
    __slots__ = (
        "channels",
        "genres"
    )

    def __init__(self, data, http):
        super().__init__(data, http)
        self.channels = [Channel(c, http=self._http) for c in data["_channels"]]
        self.genres = data["_genres"]

    @property
    def youtube_channels(self):
        return [c for c in self.channels if c.type == ChannelType.YOUTUBE]

    @property
    def instagram_channels(self):
        return [c for c in self.channels if c.type == ChannelType.INSTAGRAM]

    @property
    def tiktok_channels(self):
        return [c for c in self.channels if c.type == ChannelType.TIKTOK]

    @property
    def twitter_channels(self):
        return [c for c in self.channels if c.type == ChannelType.TWITTER]

    @property
    def twitch_channels(self):
        return [c for c in self.channels if c.type == ChannelType.TWITCH]


class RankedArtist(Artist):
    __slots__ = (
        "user_name",
        "user_id",
        "rank",
        "value"
    )

    def __init__(self, data, http):
        super().__init__(data, http)
        self.user_name = data["name"]
        self.user_id = data["userID"]
        self.rank = data["rank"]
        self.value = data["value"]

    async def get_details(self):
        data = await self._http.request(f"/artist/{self.id}")
        return DetailedArtist(data, http=self._http)
