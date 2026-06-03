from homeassistant import config_entries
from .const import DOMAIN

class ZmanimProConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Beheert de configuratie-flow voor Zmanim Pro."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Eerste stap wanneer een gebruiker de integratie toevoegt."""
        # Controleer of de integratie niet al een keer is toegevoegd
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # Maak de integratie direct aan in de UI
            return self.async_create_entry(title="Zmanim Pro", data={})

        return self.async_show_form(step_id="user")
