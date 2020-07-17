from .channel import ChannelType
from .util import parse_timestamp
from .channel import Post


class ViralPost:
    __slots__ = (
        "platform",
        "post_id",
        "timestamp",
        "type",
        "value",
        "post"
    )

    def __init__(self, data, http):
        self.platform = ChannelType(data["platform"])
        self.post_id = data["postID"]
        self.timestamp = parse_timestamp(data["timestamp"])
        self.type = data["type"]
        self.value = data["value"]

        self.post = data["_post"]
        if self.post is not None:
            self.post = Post(self.post, http)
