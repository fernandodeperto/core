"""API module used to get values from the sensor."""
import asyncio

from aiohttp import ClientSession
import async_timeout


class TFADostmannAPI:
    """TFA Dostmann device API."""

    def __init__(self, session: ClientSession, host: str, port: int) -> None:
        """Initialize."""
        self._session = session
        self._host = host
        self._port = port

    async def connect(self) -> bool:
        """Test if we can connect with the host."""
        try:
            async with async_timeout.timeout(5):
                resp = await self._session.get(f"http://{self._host}:{self._port}")
        except asyncio.TimeoutError as err:
            raise TimeoutException() from err
        else:
            return resp.status == 200

    async def get_concentration(self):
        """Get concentration from the API."""
        return 10


class TimeoutException(BaseException):
    """Error used to indicate there was a timeout."""
