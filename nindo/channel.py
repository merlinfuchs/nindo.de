from enum import Enum


class ChannelType(Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    TWITCH = "twitch"


class Channel:
    __slots__ = (
        "id",
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
        self.name = data["name"]
        self.avatar_url = data["avatar"]
        self.type = ChannelType(data["platform"])
        self.deleted = data["isDeleted"]
        self.chart_placed = data["isChartPlaced"]
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
