import asyncio
import urllib.parse

from .http import HTTPClient
from .artist import Artist, RankedArtist, DetailedArtist
from .util import AsyncIterator
from .coupon import Coupon
from .milestone import Milestone
from .viral import Viral

__all__ = (
    "NindoClient",
)


class NindoClient:
    def __init__(self, **kwargs):
        self.loop = kwargs.get("loop", asyncio.get_event_loop())
        self._http = HTTPClient(**kwargs)

    async def get_artist(self, artist_id):
        data = await self._http.request(f"/artist/{artist_id}")
        return DetailedArtist(data, http=self._http)

    def search(self, term):
        async def _to_wrap():
            data = await self._http.request(f"/search/smart/{urllib.parse.quote(term)}")
            for artists in data:
                yield Artist(artists, http=self._http)

        return AsyncIterator(_to_wrap())

    def _ranked_artists(self, path):
        async def _to_wrap():
            data = await self._http.request(path)
            for artist in data:
                yield RankedArtist(artist, http=self._http)

        return AsyncIterator(_to_wrap())

    def youtube_views_charts(self):
        return self._ranked_artists("/ranks/charts/youtube/rankViews/big")

    def youtube_likes_charts(self):
        return self._ranked_artists("/ranks/charts/youtube/rankLikes/big")

    def youtube_followers_charts(self):
        return self._ranked_artists("/ranks/charts/youtube/rankSubGain/big")

    def youtube_charts(self):
        return self._ranked_artists("/ranks/charts/youtube/rank/big")

    def instagram_likes_charts(self):
        return self._ranked_artists("/ranks/charts/instagram/rankLikes/big")

    def instagram_followers_charts(self):
        return self._ranked_artists("/ranks/charts/instagram/rankSubGain/big")

    def instagram_charts(self):
        return self._ranked_artists("/ranks/charts/instagram/rank/big")

    def tiktok_likes_charts(self):
        return self._ranked_artists("/ranks/charts/tiktok/rankLikes/big")

    def tiktok_views_charts(self):
        return self._ranked_artists("/ranks/charts/tiktok/rankViews/big")

    def tiktok_followers_charts(self):
        return self._ranked_artists("/ranks/charts/tiktok/rankSubGain/big")

    def tiktok_charts(self):
        return self._ranked_artists("/ranks/charts/tiktok/rank/big")

    def twitter_likes_charts(self):
        return self._ranked_artists("/ranks/charts/twitter/rankLikes/big")

    def twitter_retweets_charts(self):
        return self._ranked_artists("/ranks/charts/twitter/rankRetweets/big")

    def twitter_followers_charts(self):
        return self._ranked_artists("/ranks/charts/twitter/rankSubGain/big")

    def twitter_charts(self):
        return self._ranked_artists("/ranks/charts/twitter/rank/big")

    def twitch_viewers_charts(self):
        return self._ranked_artists("/ranks/charts/twitch/rankViewer/big")

    def twitch_peak_viewers_charts(self):
        return self._ranked_artists("/ranks/charts/twitch/rankPeakViewer/big")

    def twitch_followers_charts(self):
        return self._ranked_artists("/ranks/charts/twitch/rankSubGain/big")

    def twitch_charts(self):
        return self._ranked_artists("/ranks/charts/twitch/rank/big")

    def coupons(self):
        # Coupons are the only resource that is paginated
        async def _to_wrap():
            buffer = []
            offset = 0
            while True:
                if len(buffer) == 0:
                    data = await self._http.request(f"/coupons?offset={offset}")
                    buffer = [Coupon(c, http=self._http) for c in data["coupons"]]
                    if len(buffer) == 0:
                        break

                    offset += len(buffer)

                yield buffer.pop(0)

        return AsyncIterator(_to_wrap())

    def milestones(self):
        async def _to_wrap():
            data = await self._http.request("/ranks/milestones")
            for milestone in data:
                yield Milestone(milestone, http=self._http)

        return AsyncIterator(_to_wrap())

    def past_milestones(self):
        async def _to_wrap():
            data = await self._http.request("/ranks/pastMilestones")
            for milestone in data:
                yield Milestone(milestone, http=self._http)

        return AsyncIterator(_to_wrap())

    def viral(self):
        async def _to_wrap():
            data = await self._http.request("/viral")
            for viral in data:
                yield Viral(viral, http=self._http)

        return AsyncIterator(_to_wrap())
