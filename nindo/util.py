import inspect
import dateutil.parser


__all__ = (
    "maybe_coroutine",
    "AsyncIterator",
    "parse_timestamp"
)


async def maybe_coroutine(coro):
    if inspect.isawaitable(coro):
        return await coro

    return coro


class AsyncIterator:
    def __init__(self, to_wrap):
        self._to_wrap = to_wrap

    def __aiter__(self):
        return self

    def __anext__(self):
        return self._to_wrap.__anext__()

    async def flatten(self):
        return [item async for item in self]

    async def filter(self, predicate):
        async def _new_iterator():
            async for item in self:
                if await maybe_coroutine(predicate(item)):
                    yield item

        return AsyncIterator(_new_iterator())

    async def find(self, predicate):
        async for item in self:
            if await maybe_coroutine(predicate(item)):
                return item

        return None

    async def get(self, **attrs):
        def _predicate(item):
            for attr, value in attrs.items():
                nested = attr.split("__")
                element = item
                for a in nested:
                    element = getattr(element, a)

                if element != value:
                    return False

            return True

        return self.find(_predicate)

    async def map(self, func):
        async def _new_iterator():
            async for item in self:
                yield func(item)

        return AsyncIterator(_new_iterator())


def parse_timestamp(timestamp):
    if timestamp is not None:
        return dateutil.parser.parse(timestamp.strip("Z"))

    return None
