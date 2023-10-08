from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity
)
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_DOMAIN
import aiohttp
from .const import DOMAIN

from datetime import timedelta
SCAN_INTERVAL = timedelta(seconds=300)

async def async_setup_entry(hass, config_entry, async_add_entities):
    domain_data = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([Sensor(domain_data)])

class Sensor(SensorEntity):
    _attr_name = "Minute Summary"
    _attr_unique_id = f'{DOMAIN}.summary'
    _attr_should_poll: True

    def __init__(self, config):
        super().__init__()
        self.lat = config[CONF_LATITUDE]
        self.lon = config[CONF_LONGITUDE]
        self.domain = config[CONF_DOMAIN]

    async def async_update(self):
        minutely_url = f"https://d3.{self.domain}/webgis_rain_new/webgis/minute?lat={self.lat}&lon={self.lon}"
        timeout = aiohttp.ClientTimeout(total=5)
        connector = aiohttp.TCPConnector(limit=5, force_close=True)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async with session.get(minutely_url) as response:
                res = await response.json()
                
                self._attr_native_value = res.get("msg")
                self._attr_extra_state_attributes = {"uptime": res.get("uptime"), "values": res.get("values"),"start_at": res.get("times",[None])[0]}
                if res and sum(res.get("values",0)) > 0:
                    self._attr_icon = "mdi:umbrella"
                else:
                    self._attr_icon = "mdi:umbrella-closed"
                
