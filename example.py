import asyncio

from nindo import NindoClient


async def test():
    client = NindoClient()
    print("--- Youtube ---")
    async for artist in client.youtube_top():
        print(artist.rank, artist.name)

    print("--- Instagram ---")
    async for artist in client.instagram_top():
        print(artist.rank, artist.name)

    print("--- TikTok ---")
    async for artist in client.tiktok_top():
        print(artist.rank, artist.name)

    print("--- Twitter ---")
    async for artist in client.twitter_top():
        print(artist.rank, artist.name)

    print("--- Twitch ---")
    async for artist in client.twitch_top():
        print(artist.rank, artist.name)

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
