import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol


from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components.sensor import SensorEntity

from rtde.rtde_ur10_connection import UR10Listener

_LOGGER = logging.getLogger(__name__)

DOMAIN = "UR10_ha"

class UR10RobotEntity(SensorEntity):
    def __init__(self):
        self._is_on = False
        self._attr_name = "UR10"
        self._attr_unique_id = "ur10robot"
        self._attr_icon = "mdi:robot-industrial"
        self._attr_should_poll = False
        self._attr_available = True

        self.ur10_listener = UR10Listener("172.22.114.160", 125, "rtde/record_configuration.xml")
        self.booln = False

    @property
    def state(self):
        return self.booln



