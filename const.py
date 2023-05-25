"""Constants for the UR10 for home assistant integration."""
from __future__ import annotations
import logging
from datetime import timedelta


DOMAIN = "urha"
LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=1/125)
RETRY_INTERVAL = timedelta(seconds=5)
