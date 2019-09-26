"""Support for HDHomeRun devices."""
import logging

from hdhr.adapter import HdhrUtility, HdhrDeviceQuery

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HDHomeRun from a config entry."""
    hosts = hass.data[DOMAIN].get(SENSOR_DOMAIN)
    devices = []

    if hosts:
        # Priority 1: manual config
        for host in hosts:
            ip = host[CONF_HOST]
            _LOGGER.debug('Fetching devices for manually-configured host: ' + ip)
            devices.extend(HdhrUtility.discover_find_devices_custom(ip=ip))
    else:
        # Priority 2: scanned devices
        _LOGGER.debug('Scanning network for HDHomeRun devices')
        devices = HdhrUtility.discover_find_devices_custom()

    entities = []

    for device in devices:
        device_id = device.nice_device_id
        tuner_count = device.tuner_count
        _LOGGER.debug("Detected %d tuners for device: %s" % (tuner_count, device_id))

        for tuner in range(0, tuner_count):
            entities.append(TunerSensor("%s-%d" % (device_id, tuner)))

    async_add_entities(entities, update_before_add=True)

    return True

class TunerSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, device_str):
        """Initialize the sensor."""
        self._id = device_str
        self._device = HdhrUtility.device_create_from_str(device_str)
        self._adapter = HdhrDeviceQuery(self._device)
        self._state = None

    async def async_update(self):
        _LOGGER.debug('Fetching status for tuner: ' + self._id)
        (vstatus, raw_data) = self._adapter.get_tuner_vstatus()
        self._state = vstatus

    @property
    def name(self):
        """Return the name of the sensor."""
        return "HDHomeRun Channel " + self._id

    @property
    def unique_id(self):
        return self._id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state.nice_vchannel if self._state else None