"""
Support for Melissa climate.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/melissa/
"""
import logging

import voluptuous as vol

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform

REQUIREMENTS = ["py-melissa-climate==2.0.0"]

_LOGGER = logging.getLogger(__name__)

DOMAIN = "melissa"
DATA_MELISSA = 'MELISSA'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up the Melissa Climate component."""
    import melissa

    conf = config[DOMAIN]
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)
    api = melissa.AsyncMelissa(username=username, password=password)
    await api.async_connect()
    hass.data[DATA_MELISSA] = api

    hass.async_create_task(
        async_load_platform(hass, 'sensor', DOMAIN, {}, config))
    hass.async_create_task(
        async_load_platform(hass, 'climate', DOMAIN, {}, config))
    return True
