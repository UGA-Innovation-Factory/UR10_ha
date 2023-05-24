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
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            return [random.randint(0, 100) for i in range(10)]
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")