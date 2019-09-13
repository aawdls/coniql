from ._types import Channel


class Plugin:
    async def get_channel(self, channel_id: str, timeout: float) -> Channel:
        """Get the current structure of a channel"""
        raise NotImplementedError(self)

    async def put_channel(self, channel_id: str, value, timeout: float
                          ) -> Channel:
        """Put a value to a channel, returning the value after put"""
        raise NotImplementedError(self)

    async def subscribe_channel(self, channel_id: str):
        """Subscribe to the structure of the value, yielding dict structures
        where only changing top level fields are filled in"""
        yield
        raise NotImplementedError(self)

    def startup(self):
        """Start any services the plugin needs. Don't block"""

    def shutdown(self):
        """Destroy the plugin and any connections it has"""
