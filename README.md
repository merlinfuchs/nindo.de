# Python nindo.de wrapper

## Installation

```
pip install git+git://github.com/Merlintor/nindo.de
```

## Usage

```py
client = NindoClient()
async for artist in client.search("unge"):
    print(artist.name)
```

See `example.py` for more information.