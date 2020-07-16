import asyncio

from nindo import NindoClient


async def test():
    client = NindoClient()
    print("\n--- Search ---")
    async for artist in client.search("unge"):
        print(artist.name)

    print("\n--- Youtube ---")
    async for artist in client.youtube_top():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.youtube_channels))

    print("\n--- Instagram ---")
    async for artist in client.instagram_top():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.instagram_channels))

        channel = await details.instagram_channels[0].get_details()
        print("Average Comments:", channel.average_comments)

    print("\n--- TikTok ---")
    async for artist in client.tiktok_top():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.tiktok_channels))

    print("\n--- Twitter ---")
    async for artist in client.twitter_top():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.twitter_channels))

    print("\n--- Twitch ---")
    async for artist in client.twitch_top():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.twitch_channels))

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
