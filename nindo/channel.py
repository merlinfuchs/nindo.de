from enum import Enum
from datetime import timedelta
import socketio
import asyncio

from .util import parse_timestamp, AsyncIterator

__all__ = (
    "ChannelType",
    "Channel",
    "YouTubeDetails",
    "TikTokDetails",
    "InstagramDetails",
    "TwitterDetails",
    "TwitchDetails",
    "History",
    "HistoryEntry",
    "PostAnalytic",
    "Post"
)


class ChannelType(Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    TWITCH = "twitch"


class Channel:
    __slots__ = (
        "id",
        "artist_id",
        "name",
        "avatar_url",
        "type",
        "deleted",
        "chart_placed",
        "rank",
        "subscribers",
        "_http"
    )

    def __init__(self, data, http):
        self.id = data["id"]
        self.name = data.get("name")
        self.artist_id = data.get("artistID", data.get("artist_id"))
        self.avatar_url = data["avatar"]
        self.type = ChannelType(data["platform"])
        self.deleted = bool(data.get("isDeleted"))
        self.chart_placed = bool(data.get("isChartPlaced"))
        self.rank = data.get("rank")
        self.subscribers = data.get("subscribers")

        self._http = http

    async def get_details(self):
        data = await self._http.request(f"/channel/{self.type.value}/{self.id}")
        if self.type == ChannelType.YOUTUBE:
            return YouTubeDetails(data, self._http)

        elif self.type == ChannelType.INSTAGRAM:
            return InstagramDetails(data, self._http)

        elif self.type == ChannelType.TIKTOK:
            return TikTokDetails(data, self._http)

        elif self.type == ChannelType.TWITTER:
            return TwitterDetails(data, self._http)

        elif self.type == ChannelType.TWITCH:
            return TwitchDetails(data, self._http)

    async def get_history(self):
        data = await self._http.request(f"/channel/historic/{self.type.value}/{self.id}")
        return History.from_data(data)

    def posts(self):
        async def _to_wrap():
            data = await self._http.request(f"/posts/{self.type.value}/{self.id}")
            for post in data:
                yield Post(post)

        return AsyncIterator(_to_wrap())

    async def live(self):
        sio = socketio.AsyncClient()

        events = asyncio.Queue()

        @sio.on(event="subscribers")
        async def _on_stats(*args):
            await events.put(args[-1])

        await sio.connect("wss://subs.nindo.de/socket.io")
        await sio.emit("subscribe", (self.type.value, self.id))
        while True:
            try:
                yield await asyncio.wait_for(events.get(), timeout=10)
            except Exception as e:
                await sio.disconnect()
                raise e

    async def get_artist(self):
        # Reverse lookup
        from .artist import DetailedArtist
        data = await self._http.request(f"/artist/{self.artist_id}")
        return DetailedArtist(data, http=self._http)


class YouTubeDetails(Channel):
    pass


class InstagramDetails(Channel):
    __slots__ = (
        "average_comments",
        "average_engagement",
        "average_likes",
        "last_post",
        "comments_rank",
        "likes_rank",
        "followers_rank",
        "recent_shitstorm",
        "regular_clickbait",
        "regular_fsk18",
        "followers_last_month",
        "posts_last_month",
        "stories_last_month",
        "total_igtv",
        "total_posts",
        "verified"
    )

    def __init__(self, data, http):
        super().__init__(data, http)
        self.average_comments = data["avgComments5"]
        self.average_engagement = data["avgEngagement5"]
        self.average_likes = data["avgLikes5"]
        self.last_post = data["lastPost"]
        self.comments_rank = data["rankComments"]
        self.likes_rank = data["rankLikes"]
        self.followers_rank = data["rankSubGain"]
        self.recent_shitstorm = data["recentShitstorm"]
        self.regular_clickbait = data["regularClickbait"]
        self.regular_fsk18 = data["regularFSK18"]
        self.followers_last_month = data["subGain30"]
        self.posts_last_month = data["sumPosts30"]
        self.stories_last_month = data["sumStories30"]
        self.total_igtv = data["totalIGTV"]
        self.total_posts = data["totalPosts"]
        self.verified = bool(data["verified"])


class TikTokDetails(Channel):
    pass


class TwitterDetails(Channel):
    pass


class TwitchDetails(Channel):
    pass


class HistoryEntry:
    __slots__ = (
        "followers",
        "timestamp"
    )

    def __init__(self, data):
        self.followers = data["followers"] or -1
        self.timestamp = parse_timestamp(data["timestamp"])


class History:
    __slots__ = (
        "entries"
    )

    def __init__(self, entries):
        self.entries = entries

    @classmethod
    def from_data(cls, data):
        return cls([HistoryEntry(e) for e in data])

    def before(self, timestamp):
        return History([
            e
            for e in self.entries
            if e.timestamp < timestamp
        ])

    def after(self, timestamp):
        return History([
            e
            for e in self.entries
            if e.timestamp > timestamp
        ])

    def daily_change(self):
        pass

    def weekly_change(self):
        pass

    @property
    def total_change(self):
        if len(self.entries) > 1:
            return self.entries[-1].followers - self.entries[0].followers

        return 0

    @property
    def time_span(self):
        if len(self.entries) > 1:
            return self.entries[-1].timestamp - self.entries[0].timestamp

        return timedelta()


class PostAnalytic:
    __slots__ = (
        "age",
        "type",
        "channel_id",
        "id",
        "post_id",
        "value"
    )

    def __init__(self, data):
        self.age = timedelta(days=data["age"])
        self.type = data["analyticsType"]
        self.channel_id = data["channelID"]
        self.id = data["id"]
        self.post_id = data["postID"]
        self.value = data["value"]


class Post:
    __slots__ = (
        "content",
        "description",
        "post_id",
        "published",
        "analytics",
        "_http"
    )

    def __init__(self, data):
        self.content = data["content"]
        self.description = data["description"]
        self.post_id = data["postID"]
        self.published = parse_timestamp(data["published"])
        self.analytics = [PostAnalytic(a) for a in data.get("_analytics", [])]
