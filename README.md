# Python nindo.de wrapper

Some parts of the internal Nindo-Api are pretty inconsistent (For example some properties are snake- and some are camel-case (╯°□°)╯︵ ┻━┻).  
That's why some of the constructors are pretty messy ...  
  
This library is a product of reverse engineering and highly untested. Please create an issue if you encounter a bug.

## Features

- [x] Artist Retrieval
- [x] Search
- [x] Charts
- [x] Artist Details
- [ ] Channel Details
- [x] Channel History
- [x] Channel Posts
- [x] Live Websocket
- [x] Viral
- [x] Coupons
- [x] Milestones

## Installation

```
pip install git+git://github.com/Merlintor/nindo.de
```

## Usage

All the examples need to be executed in an async context.
Many functions return an async iterator which supports manipulation like `.filter`, `.map` and more. 
See `util.py` for all available functions.

### Search

```py
client = NindoClient()
async for artist in client.search("unge"):
    print(artist.name)
```

### Charts

```py
client = NindoClient()
async for artists in client.youtube_charts():
    print(artist.name)
```

### Channel History

```py
client = NindoClient()
# Get an artist by id
await client.get_artist("fe23cce0bcdb3d89cbfd500d91487202")
# Get the first instagram channel of the artist
channel = artist.instagram_channels[0]
# Get the channel history
history = await channel.get_history()

# Print the count of entries
print(len(history.entries)
# Print the total follower change over the time span
print(history.time_span, history.total_change)
```

### Live Followers

This only seems to work for channels that appear at the top of the milestones.

```py
client = NindoClient()
# Get an artist by id
await client.get_artist("fe23cce0bcdb3d89cbfd500d91487202")
# Get the first instagram channel of the artist
channel = artist.instagram_channels[0]

# Print each follower update
async for follower in channel.live():
    print(follower)
```

See `example.py` for more information.