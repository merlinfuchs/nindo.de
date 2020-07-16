import asyncio
from datetime import datetime

from nindo import NindoClient


async def test():
    client = NindoClient()
    print("\n--- Milestones ---")
    async for milestone in client.milestones():
        print(milestone.expected_time, milestone.followers)

    print("\n--- Coupons ---")
    async for coupon in client.coupons():
        print(coupon.discount, coupon.code)

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

        channel = details.instagram_channels[0]
        channel_details = await channel.get_details()
        print("Average Comments:", channel_details.average_comments)

        channel_history = await channel.get_history()
        print("History Change:", channel_history.before(datetime.utcnow()).total_change)

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
