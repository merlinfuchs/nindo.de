import asyncio
from datetime import datetime

from nindo import NindoClient


async def test():
    client = NindoClient()

    print("\n--- Viral ---")
    async for viral in client.viral():
        print(viral.type, viral.post.title)

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
    async for artist in client.youtube_charts():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.youtube_channels))

    print("\n--- Instagram ---")
    async for artist in client.instagram_charts():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.instagram_channels))

        channel = details.instagram_channels[0]
        channel_details = await channel.get_details()
        print("Average Comments:", channel_details.average_comments)

        channel_history = await channel.get_history()
        print("History Change:", channel_history.before(datetime.utcnow()).total_change)

        post_count = await channel.posts().flatten()
        print("Post Count:", len(post_count))

    print("\n--- TikTok ---")
    async for artist in client.tiktok_charts():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.tiktok_channels))

    print("\n--- Twitter ---")
    async for artist in client.twitter_charts():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.twitter_channels))

    print("\n--- Twitch ---")
    async for artist in client.twitch_charts():
        print("\n", artist.rank, artist.name)
        details = await artist.get_details()
        print("Channels:", len(details.twitch_channels))

    print("\n--- Live ---")
    artist = await client.get_artist("fe23cce0bcdb3d89cbfd500d91487202")
    channel = artist.instagram_channels[0]
    async for followers in channel.live():
        print(followers)

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
