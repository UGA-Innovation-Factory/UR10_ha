"""The UR10 for home assistant integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import async_call_later
from homeassistant.const import Platform
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import DOMAIN, LOGGER, RETRY_INTERVAL
from .coordinator import UR10Coordinator

from .rtde_ur10_connection import UR10Listener
from .rtde import RTDEException

PLATFORMS: list[Platform] = [Platform.SENSOR]

# TODO: rewrite functionality to work with Config entries and Config Flow
# Why? Because most porper functionality and helpers of HA depend on having Config entries set up

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""

    async def retry_setup(now):
        """Retry setup if a connection/timeout happens on Slide API."""
        hass.data[DOMAIN] = {"retrying_setup": True}
        await async_setup(hass, config)

    ur10conn = UR10Listener("172.22.114.160", 100)
    coordinator = UR10Coordinator(hass, ur10conn)

    try:
        ur10conn.connect()
        await coordinator.async_refresh()

        if coordinator.data == None:
            await coordinator.async_refresh()

        if coordinator.data == None:
            raise UpdateFailed("Error: no data from UR10")


    except Exception as err:
        if not DOMAIN in hass.data:
            LOGGER.error(
                "Error connecting to UR10: %s. Will try again in %s second(s)",
                err,
                RETRY_INTERVAL.total_seconds(),
            )
        ur10conn.disconnect()
        async_call_later(hass, RETRY_INTERVAL, retry_setup)
        return True



    # Data that you want to share with your platforms
    hass.data[DOMAIN] = {"urhacoordinator": coordinator}

    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)

    return True