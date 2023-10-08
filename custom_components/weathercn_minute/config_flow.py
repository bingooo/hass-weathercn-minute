from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from homeassistant.const import (
    CONF_DOMAIN,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    return {"title": DOMAIN}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        DATA_SCHEMA = vol.Schema({
            vol.Required(CONF_DOMAIN): str,
            vol.Optional(CONF_LONGITUDE, default=self.hass.config.longitude): cv.longitude,
            vol.Optional(CONF_LATITUDE, default=self.hass.config.latitude): cv.latitude
        })

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )