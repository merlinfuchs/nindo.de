# Python nindo.de wrapper

Some parts of the internal Nindo-Api are pretty inconsistent (For example some properties are snake- and some are camel-case (╯°□°)╯︵ ┻━┻).  
That's why some of the constructors are pretty messy ...

## Features

- [x] Artist Retrieval
- [x] Search
- [x] Charts
- [x] Artist Details
- [ ] Channel Details
- [x] Channel History
- [ ] Channel Posts
- [ ] Live Websocket (Help Needed)
- [ ] Viral
- [x] Coupons
- [x] Milestones

## Installation

```
pip install git+git://github.com/Merlintor/nindo.de
```

## Usage

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

See `example.py` for more information.