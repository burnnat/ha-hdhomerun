"""Config flow for HDHomeRun."""
from homeassistant.helpers import config_entry_flow
from homeassistant import config_entries

try:
    from hdhr.adapter import HdhrUtility
except ModuleNotFoundError:
    _LOGGER.exception(
        '''libhdhomerun missing: install with:
            sudo docker exec -it homeassistant bash
            apk add libhdhomerun'''
    )

from .const import DOMAIN


async def _async_has_devices(hass):
    """Return if there are devices that can be discovered."""
    hdhr_devices = HdhrUtility.discover_find_devices_custom()
    return len(hdhr_devices) > 0


@config_entries.HANDLERS.register(DOMAIN)
class HDHomeRunConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user step."""
