# import logging
# import homeassistant.helpers.config_validation as cv
# import voluptuous as vol
# import random


# from homeassistant.core import HomeAssistant
# from homeassistant.const import CONF_NAME
# from homeassistant.helpers.entity_component import EntityComponent
# from homeassistant.components.sensor import SensorEntity

# #from rtde.rtde_ur10_connection import UR10Listener

# _LOGGER = logging.getLogger(__name__)

# DOMAIN = "urha"

# class UR10RobotEntity(SensorEntity):
#     def __init__(self, name):
#         self._is_on = False
#         self._attr_name = name
#         self._attr_unique_id = name
#         self._attr_has_entity_name = True
#         self._attr_icon = "mdi:robot-industrial"
#         self._state = None

#         #self.ur10_listener = UR10Listener("172.22.114.160", 125, "rtde/record_configuration.xml")
#         #self.booln = False

#     @property
#     def state(self):
#         return self._state
    
#     def update(self):
#         #self._state = self.ur10_listener.get_all_data()
#         self._state = random.randint(0, 100)
#         pass


# async def async_setup(hass: HomeAssistant, config: dict):
#     component = EntityComponent(_LOGGER, DOMAIN, hass)

#     await component.async_add_entities([UR10RobotEntity("ur_10")])

#     return True


"""Example integration using DataUpdateCoordinator."""

from datetime import timedelta
import logging
import random
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

DOMAIN = "urha"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Config entry example."""
    # assuming API object stored here by __init__.py
    # my_api = hass.data[DOMAIN][entry.entry_id]
    coordinator = MyCoordinator(hass)

    # Fetch initial data so we have data when entities subscribe
    #
    # If the refresh fails, async_config_entry_first_refresh will
    # raise ConfigEntryNotReady and setup will try again later
    #
    # If you do not want to retry setup on failure, use
    # coordinator.async_refresh() instead
    #
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        MyEntity(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="My sensor",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
        )
        self.my_api = "UR10 instance here"

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                # Grab active context variables to limit data required to be fetched from API
                # Note: using context is not required if there is no need or ability to limit
                # data retrieved from API.
                listening_idx = set(self.async_contexts())
                return await listening_idx# self.my_api.fetch_data(listening_idx)
        except Exception as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            raise ConfigEntryAuthFailed from err
        #except Exception as err:
        #    raise UpdateFailed(f"Error communicating with API: {err}")


class MyEntity(CoordinatorEntity, SensorEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx
        self._state = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._state = self.coordinator.data[self.idx]["state"]
        self.async_write_ha_state()

    # async def async_turn_on(self, **kwargs):
    #     """Turn the light on.

    #     Example method how to request data updates.
    #     """
    #     # Do the turning on.
    #     # ...

    #     # Update the data
    #     await self.coordinator.async_request_refresh()