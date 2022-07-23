"""Config flow for AirCo2ntrol Coach integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import aiohttp_client

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ADDRESS): str,
        vol.Required(CONF_PORT): int,
    }
)


class PlaceholderHub:
    """Placeholder class to make tests pass."""

    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        """Initialize."""
        self._hass = hass
        self._host = host
        self._port = port

    async def connect(self) -> bool:
        """Test if we can connect with the host."""
        session = aiohttp_client.async_get_clientsession(self._hass)

        try:
            async with async_timeout.timeout(5):
                resp = await session.get(f"http://{self._host}:{self._port}")
        except asyncio.TimeoutError as err:
            raise CannotConnect() from err
        else:
            return resp.status == 200


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    hub = PlaceholderHub(hass, data[CONF_HOST], data[CONF_PORT])

    if not await hub.connect():
        raise CannotConnect()

    # Return info that you want to store in the config entry.
    return {"title": "Name of the device"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AirCo2ntrol Coach."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
