"""DataUpdateCoordinator for urha"""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, LOGGER, SCAN_INTERVAL, RETRY_INTERVAL
from .rtde_ur10_connection import UR10Listener


class UR10Coordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass: HomeAssistant, urconnection: UR10Listener) -> None:
        """Initialize my coordinator."""
        self.urconnection = urconnection
        super().__init__(
            hass,
            LOGGER,
            name=f"{DOMAIN}coord",
            update_interval=SCAN_INTERVAL,
        )
        self.printedError = False

    async def _async_update_data(self):
        """Fetch data"""
        try:
            self.update_interval = SCAN_INTERVAL
            if not self.urconnection.is_connected():
                self.urconnection.connect()
                self.printedError = False
                LOGGER.info("Reconnected to UR10 successfully")

            return self.urconnection.read_dict_flat()

        except Exception as err:
            self.update_interval = RETRY_INTERVAL
            self.urconnection.disconnect()
            if not self.printedError:
                self.printedError = True
                LOGGER.error("Error connecting to UR10: %s. Will try again every %s second(s)",
                    err,
                    RETRY_INTERVAL.total_seconds(),)
            raise UpdateFailed(f"Error communicating with UR10: {err}") from err