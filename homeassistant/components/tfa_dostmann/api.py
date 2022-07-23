"""API module used to get values from the sensor."""


class TFADostmannAPI:
    """Implementation of a basic API based on a Home Assistant entity config."""

    def __init__(self) -> None:
        """Initialize."""

    async def get_concentration(self):
        """Get concentration from the API."""
        return 10
