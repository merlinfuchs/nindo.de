from .util import parse_timestamp
from .channel import Channel

__all__ = (
    "Milestone",
)


class Milestone:
    __slots__ = (
        "followers",
        "expected_time",
        "channel"
    )

    def __init__(self, data, http):
        self.followers = data["currentSubs"]
        self.expected_time = parse_timestamp(data["expectedTime"])
        self.channel = data.get("_channel")
        if self.channel is not None:
            self.channel = Channel(self.channel, http)
