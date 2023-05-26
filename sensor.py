"""CoordinatorEntity sensor for urha"""
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import callback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN
from .coordinator import UR10Coordinator


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info = None,
) -> None:
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    coordinator: UR10Coordinator = hass.data[DOMAIN]["urhacoordinator"]
    add_entities(MyEntity(coordinator, key) for key, v in coordinator.data.items())


class MyEntity(CoordinatorEntity, SensorEntity):
    """SensorEntity for urha."""

    def __init__(self, coordinator, idx) -> None:
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.idx = idx
        self._attr_icon = "mdi:robot-industrial"
        self._attr_name = f"ur10_{idx}"
        self._attr_unique_id = f"ur10_{idx}"
        self._attr_state_class = "measurement"
        self._state = 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._state = self.coordinator.data[self.idx]
        self.async_write_ha_state()

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state