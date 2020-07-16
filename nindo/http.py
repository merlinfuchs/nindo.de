import asyncio
import aiohttp


__all__ = (
    "HTTPClient",
)


class HTTPClient:
    BASE_URL = "https://api.nindo.de"

    def __init__(self, **kwargs):
        self.loop = kwargs.get("loop", asyncio.get_event_loop())
        self.session = kwargs.get("session", aiohttp.ClientSession(loop=self.loop))

    async def request(self, path, method="GET", **kwargs):
        async with self.session.request(
                method=method,
                url=f"{self.BASE_URL}{path}",
                **kwargs
        ) as resp:
            resp.raise_for_status()
            return await resp.json()
