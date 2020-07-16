from .artist import Artist
from .util import parse_timestamp

__all__ = (
    "Brand",
    "Coupon",
)


class Brand:
    __slots__ = (
        "id",
        "branch",
        "color",
        "name",
        "url"
    )

    def __init__(self, data):
        self.id = data["id"]
        self.branch = data["branch"]
        self.color = data["color"]
        self.name = data["name"]
        self.url = data["url"]


class Coupon:
    __slots__ = (
        "artist_id",
        "brand_id",
        "code",
        "discount",
        "id",
        "terms",
        "timestamp",
        "url",
        "valid",
        "valid_until",
        "artist",
        "brand",
        "_http"
    )

    def __init__(self, data, http):
        self.artist_id = data["artistID"]
        self.brand_id = data["brandID"]
        self.code = data["code"]
        self.discount = data["discount"]
        self.id = data["id"]
        self.terms = data.get("terms")
        self.timestamp = parse_timestamp(data["timestamp"])
        self.url = data.get("url")
        self.valid = data["valid"]
        self.valid_until = parse_timestamp(data.get("validUntil"))

        self.artist = data.get("_artist")
        if self.artist is not None:
            self.artist = Artist(self.artist, http)

        self.brand = data.get("_brand")
        if self.brand is not None:
            self.brand = Brand(self.brand)

        self._http = http
