from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.http import HomeAssistantView

from .date_provider import DateProvider
from .sensors_data import GregorianDateSensor, JewishDateSensor
from .sensors_feestdagen import JewishHolidaySensor
from .sensors_tijden import ZmanimTimeSensor
from .__init__ import ZmanimApiView # Laad de view in

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_platform(
    hass: HomeAssistant, 
    config: dict, 
    async_add_entities: AddEntitiesCallback, 
    discovery_info=None
) -> None:
    """Zet alle Zmanim Pro sensoren en de API klaar."""
    provider = DateProvider()
    
    # REGISTREER DE API RECHTSTREEKS VANUIT DE SENSOR SETUP
    try:
        _LOGGER.info("Zmanim Pro API handmatig registreren via sensor platform...")
        hass.http.register_view(ZmanimApiView(hass))
    except Exception as e:
        _LOGGER.error("Kon API View niet registreren via sensor.py: %s", e)
    
    lijst_van_sensoren = [
        GregorianDateSensor(provider),
        JewishDateSensor(provider),
        JewishHolidaySensor(provider),
        ZmanimTimeSensor(provider, "shkia", "Shkia (Zonsondergang)", "mdi:weather-sunset"),
        ZmanimTimeSensor(provider, "chatzos", "Chatzos (Middag)", "mdi:weather-sunny"),
        ZmanimTimeSensor(provider, "sof_zman_krias_shema", "Krias Shema (Grá)", "mdi:book-open-variant", "gra"),
        ZmanimTimeSensor(provider, "sof_zman_krias_shema", "Krias Shema (Magen Avraham)", "mdi:book-open-page-variant", "magen_avraham"),
        ZmanimTimeSensor(provider, "sof_zman_tefila", "Sof Zman Tefila (Grá)", "mdi:clock-outline", "gra"),
        ZmanimTimeSensor(provider, "sof_zman_tefila", "Sof Zman Tefila (Magen Avraham)", "mdi:clock-check-outline", "magen_avraham"),
        ZmanimTimeSensor(provider, "plag_hamincha", "Plag HaMincha (Grá)", "mdi:weather-sunset-down", "pla_gra"),
        ZmanimTimeSensor(provider, "plag_hamincha", "Plag HaMincha (Magen Avraham)", "mdi:weather-sunset-up", "plag_magen_avraham")
    ]
    
    async_add_entities(lijst_van_sensoren, True)
