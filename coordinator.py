from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, LOGGER, SCAN_INTERVAL

import random

class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry):
        """Initialize my coordinator."""
        self.config_entry = config_entry
        super().__init__(
            hass,
            LOGGER,
            name="urhacoordinator",
            update_interval=SCAN_INTERVAL,
        )


    async def _async_update_data(self):
        """Fetch data"""
        return [random.randint(0, 100) for i in range(10)]