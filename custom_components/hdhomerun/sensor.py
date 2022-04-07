"""Support for HDHomeRun devices."""
import logging

from enum import IntEnum

from hdhr.adapter import HdhrUtility, HdhrDeviceQuery, OperationRejectedError

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, CONF_HOST

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

        adapter = HdhrDeviceQuery(HdhrUtility.device_create_from_str(device_id))

        device_info = {
            'identifiers': {
                (DOMAIN, device_id)
            },
            'name': 'HDHomeRun ' + device_id,
            'manufacturer': 'SiliconDust',
            'model': adapter.get_model_str(),
            'sw_version': adapter.get_version(),
        }

        for tuner in range(0, tuner_count):
            tuner_str = "%s-%d" % (device_id, tuner)
            entities.append(TunerSensor(device_info, tuner_str))

    async_add_entities(entities, update_before_add=True)

    return True


class TunerSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, parent_info, device_str):
        """Initialize the sensor."""
        self._id = device_str
        self._device_info = parent_info
        self._adapter = HdhrDeviceQuery(
            HdhrUtility.device_create_from_str(device_str))
        self._state = None
        self._extra_state_attributes = {}

    async def async_update(self):
        _LOGGER.debug(
            'Updating tuner: %s',
            self._id)
        stream_info = self._adapter.get_tuner_streaminfo()
        if len(stream_info) != 0:
            program = self._adapter.get_tuner_program()
            channel = program
            channel_name = None
            for stream in stream_info:
                if stream.program == program:
                    channel = stream.vchannel
                    channel_name = stream.name
            (status, raw_data) = self._adapter.get_tuner_status()
            # there are errors in the mapping of raw_date to status, we do it ourselves
            new_status = {}
            for x in str(raw_data).split(' '):
                snippet = x.split('=')
                new_status.update({snippet[0]: snippet[1]})
            if channel_name:
                self._state = channel+' '+channel_name
            else:
                self._state = channel
            self._extra_state_attributes['signal_strength'] = new_status['ss']
            self._extra_state_attributes['snr'] = new_status['snq']
            self._extra_state_attributes['bps'] = new_status['bps']
        else:
            self._state = 'not in use'

    @property
    def name(self):
        """Return the name of the sensor."""
        return "HDHomeRun Tuner " + self._id

    @property
    def unique_id(self):
        return self._id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        return self._device_info

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._extra_state_attributes
