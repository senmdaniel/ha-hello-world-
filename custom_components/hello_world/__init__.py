from .panel import async_setup_panel

async def async_setup(hass, config):
    await async_setup_panel(hass)
    return True
