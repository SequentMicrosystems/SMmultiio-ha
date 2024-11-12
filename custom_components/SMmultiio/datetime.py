DEFAULT_ICONS = {
        "on": "mdi:clock",
        "off": "mdi:clock-alert",
}

import logging
import time
import types
import inspect
from inspect import signature
import requests

from homeassistant.components.datetime import DateTimeEntity
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.event import async_track_time_interval
import homeassistant.util.dt as ha_dt
from datetime import timedelta, datetime

from . import (
        DOMAIN, CONF_STACK, CONF_TYPE, CONF_CHAN, CONF_NAME,
        CONF_UPDATE_INTERVAL,
        SM_MAP, SM_API
)
SM_MAP = SM_MAP["datetime"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, add_devices, discovery_info=None):
    # We want this platform to be setup via discovery
    if discovery_info == None:
        return
    add_devices([DateTime(
        hass=hass,
		name=discovery_info.get(CONF_NAME),
        stack=discovery_info.get(CONF_STACK),
        type=discovery_info.get(CONF_TYPE),
        chan=discovery_info.get(CONF_CHAN),
        update_interval=discovery_info.get(CONF_UPDATE_INTERVAL) or 30,
	)])

class DateTime(DateTimeEntity):
    def __init__(self, hass, name, stack, type, chan, update_interval):
        generated_name = DOMAIN + str(stack) + "_" + type + "_" + str(chan)
        self._unique_id = generate_entity_id("datetime.{}", generated_name, hass=hass)
        self._name = name or generated_name
        self._stack = int(stack)
        self._type = type
        self._chan = int(chan)
        self._update_interval = float(update_interval)
        self._short_timeout = .05
        self._icons = DEFAULT_ICONS | SM_MAP[self._type].get("icon", {})
        self._icon = self._icons["off"]
        self._uom = SM_MAP[self._type].get("uom", "")
        self._value = 0
        self._remove_hooks = []
        self.__SM__init()
        ### __CUSTOM_SETUP__ START
        ### __CUSTOM_SETUP__ END

    def __SM__init(self):
        com = SM_MAP[self._type]["com"]
        self._SM = SM_API
        if inspect.isclass(self._SM):
            self._SM = self._SM(self._stack)
            self._SM_get = getattr(self._SM, com["get"])
            self._SM_set = getattr(self._SM, com["set"])
        else:
            _SM_get = getattr(self._SM, com["get"])
            _SM_set = getattr(self._SM, com["set"])
            def _aux_SM_get(*args):
                return _SM_get(self._stack, *args)
            self._SM_get = _aux_SM_get
            def _aux3_SM_set(*args):
                return _SM_set(self._stack, *args)
            self._SM_set = _aux3_SM_set

    async def async_added_to_hass(self):
        new_hook = async_track_time_interval(
                self.hass, self.async_update_ha_state, timedelta(seconds=self._update_interval)  # type: ignore[arg-type]
        )
        self._remove_hooks.append(new_hook)

    async def async_will_remove_from_hass(self):
        for remove_hook in self._remove_hooks:
            remove_hook()

    @property
    def should_poll(self): # type: ignore[override]
        return False

    def update(self):
        time.sleep(self._short_timeout)
        try:
            date_tuple = self._SM_get(self._chan)
            self._value = datetime(*date_tuple)
            try:
                requests.get("http://www.google.com", timeout=3)
                has_internet = True
            except requests.ConnectionError:
                has_internet = False
            if has_internet:
                ha_time = ha_dt.now()
                self._SM_set(ha_time.year, ha_time.month, ha_time.day, ha_time.hour, ha_time.minute, ha_time.second)
                self._value = ha_time
                _LOGGER.error(f"{DOMAIN} RTC updated to {self._value} from HA time")

        except Exception as ex:
            _LOGGER.error(DOMAIN + " %s update() failed, %e, %s, %s", self._type, ex, str(self._stack), str(self._chan))
            return
        if self._value != 0:
            self._icon = self._icons["on"]
        else:
            self._icon = self._icons["off"]

    def set_value(self, value: datetime) -> None:
        self._SM_set(value.year, value.month, value.day, value.hour, value.minute, value.second)
        self._value = value

    @property
    def unique_id(self): # type: ignore[override]
        return self._unique_id

    @property
    def name(self): # type: ignore[override]
        return self._name

    @property
    def icon(self): # type: ignore[override]
        return self._icon

    @property
    def native_unit_of_measurement(self):
        return self._uom

    @property
    def native_value(self): # type: ignore[override]
        return self._value
