"""Support for HDHomeRun devices."""
import logging
from enum import IntEnum
from hdhr.adapter import HdhrUtility, HdhrDeviceQuery, OperationRejectedError

# from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
# from homeassistant.helpers.entity import Entity

# from .const import DOMAIN, CONF_HOST
DOMAIN = 'TEST'


class StatusApi(IntEnum):
    # Note that these APIs are in fallback order
    VSTATUS = 1
    STREAMINFO = 2
    STATUS = 3


class TunerSensor:
    """Representation of a Sensor."""

    def __init__(self, parent_info, device_str):
        """Initialize the sensor."""
        self._id = device_str
        self._device_info = parent_info
        self._adapter = HdhrDeviceQuery(
            HdhrUtility.device_create_from_str(device_str))
        self._status_api = StatusApi(1)
        self._state = None

    async def async_update(self):
        self._state = self.fetch_channel()

    def fetch_channel(self):
        while True:
            try:
                return self.fetch_channel_raw()
            except OperationRejectedError:
                has_fallback = self.switch_fallback_api()

                if not has_fallback:
                    raise

    def switch_fallback_api(self):
        try:
            next_api = StatusApi(self._status_api + 1)
            _LOGGER.debug(
                'Operation %s not supported, falling back to %s for tuner: %s',
                self._status_api.name,
                next_api.name,
                self._id)
            self._status_api = next_api
            return True
        except ValueError:
            return False

    def fetch_channel_raw(self):
        _LOGGER.debug(
            'Fetching %s for tuner: %s',
            self._status_api.name,
            self._id)

        if self._status_api == StatusApi.VSTATUS:
            (vstatus, raw_data) = self._adapter.get_tuner_vstatus()
            return vstatus.nice_vchannel
        
        elif self._status_api == StatusApi.STREAMINFO:
            streaminfo = self._adapter.get_tuner_streaminfo()

            if not streaminfo:
                return None

            program = self._adapter.get_tuner_program()
            active = next(x for x in streaminfo if x.program == program)
            return active.vchannel

        elif self._status_api == StatusApi.STATUS:
            (status, raw_data) = self._adapter.get_tuner_status()
            return status.nice_channel
        
        else:
            raise 'Unknown status API: ' + str(self._status_api)

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


if __name__ == '__main__':
    _LOGGER = logging.getLogger(__name__)
    devices = []
    devices.extend(HdhrUtility.discover_find_devices_custom(ip='192.168.4.33'))
    # devices = HdhrUtility.discover_find_devices_custom()
    entities = []
    for device in devices:
        device_id = device.nice_device_id
        tuner_count = device.tuner_count
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
            hd = HdhrUtility.device_create_from_str(tuner_str)
            device_adapter = HdhrDeviceQuery(hd)
            streaminfo = device_adapter.get_tuner_streaminfo()
            print('streaminfo', streaminfo)
            if len(streaminfo) != 0:
                program = device_adapter.get_tuner_program()
                print("Program ", program)
                channel = None
                channel_name = None
                for stream in streaminfo:
                    if stream.program == program:
                        channel = stream.vchannel
                        channel_name = stream.name
                print("Active Channel on tuner:", tuner_str, channel, channel_name)
                (status, raw_data) = device_adapter.get_tuner_status()
                # there are errors in the mapping of raw_date to status, we do it ourselves
                new_status = {}
                for x in str(raw_data).split(' '):
                    snippet = x.split('=')
                    new_status.update({snippet[0]:snippet[1]})
                signal_strength = new_status['ss']
                snr = new_status['snq']
                bps = new_status['bps']
                print("Signal strength: ", signal_strength)
                print("SNR: ", snr)
                print("Data rate: ", bps)

            else:
                print("Tuner not locked: ", tuner_str)
    print(len(entities), 'found', '\n')