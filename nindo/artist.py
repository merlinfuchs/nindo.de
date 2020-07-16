class Artist:
    __slots__ = (
        "id",
        "name",
        "avatar_url",
        "_http"
    )

    def __init__(self, data, http):
        self.id = data["artistID"]
        self.name = data["name"]
        self.avatar_url = data["avatar"]

        self._http = http


class DetailedArtist(Artist):
    __slots__ = (
        "_channels",
        "genres"
    )

    def __init__(self, data, http):
        super().__init__(data, http)
        self._channels = data["_channels"]
        self.genres = data["_genres"]


class RankedArtist(Artist):
    __slots__ = (
        "user_name",
        "user_id",
        "rank",
        "value"
    )

    def __init__(self, data, http):
        super().__init__(data, http)
        self.user_name = data["name"]
        self.user_id = data["userID"]
        self.rank = data["rank"]
        self.value = data["value"]
