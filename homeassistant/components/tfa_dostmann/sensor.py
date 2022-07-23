"""Support for TFA Dostmann Coach data."""
from __future__ import annotations

import logging

import async_timeout

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    ATTR_FRIENDLY_NAME,
    CONCENTRATION_PARTS_PER_MILLION,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import TFADostmannAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Data provided by TFA Dostmann AirCo2ntrol Coach"
FRIENDLY_NAME = "AirCo2ntrol Coach"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Sensor Setup."""
    api: TFADostmannAPI = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([TFADostmannCO2Sensor(api)], True)


class TFADostmannCO2Sensor(SensorEntity):
    """Entity object for the CO2 sensor."""

    _attr_device_class = SensorDeviceClass.CO2
    _attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, api: TFADostmannAPI) -> None:
        """Initialize."""
        self._api: TFADostmannAPI = api
        self._concentration: int = -1
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_FRIENDLY_NAME: FRIENDLY_NAME,
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return FRIENDLY_NAME

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._concentration

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_update(self):
        """Get the CO2 data from the API."""
        async with async_timeout.timeout(5):
            self._concentration = await self._api.get_concentration()

        _LOGGER.debug("CO2 concentration: %d", self._concentration)
