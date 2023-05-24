from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import callback

from .const import DOMAIN
from .coordinator import MyCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: MyCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(MyEntity(coordinator, idx) for idx, _ in enumerate(coordinator.data))




class MyEntity(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.idx = idx
        self._attr_name = f"ur10sensor{idx}"
        self._attr_unique_id = f"ur10sensor{idx}"
        self._attr_state = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_state = self.coordinator.data[self.idx]
        self.async_write_ha_state()

    # async def async_turn_on(self, **kwargs):
    #     """Turn the light on.

    #     Example method how to request data updates.
    #     """
    #     # Do the turning on.
    #     # ...

    #     # Update the data
    #     await self.coordinator.async_request_refresh()