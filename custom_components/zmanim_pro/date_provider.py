from datetime import date
import homeassistant.util.dt as dt_util

class DateProvider:
    """Levert de juiste datum aan de Zmanim sensoren."""

    def __init__(self):
        pass

    def get_current_date(self) -> date:
        """
        Haalt de huidige datum op via de interne Home Assistant klok.
        Dit houdt direct rekening met de ingestelde tijdzone in HA.
        """
        # dt_util.now() geeft de exacte lokale tijd binnen Home Assistant
        return dt_util.now().date()

    def get_current_jewish_month(self) -> int:
        """Berekent de huidige Joodse maand op basis van de HA datum."""
        h_date = self.get_current_date()
        
        # PAS DIT AAN: Roep hier jouw eigen 'core' omrekenmethode aan!
        # Bijvoorbeeld:
        # return core.convert_to_jewish(h_date).month
        return 1  # Tijdelijke testwaarde (Maand 1 = Nissan)

    def get_current_jewish_day(self) -> int:
        """Berekent de huidige Joodse dag op basis van de HA datum."""
        h_date = self.get_current_date()
        
        # PAS DIT AAN: Roep hier jouw eigen 'core' omrekenmethode aan!
        # Bijvoorbeeld:
        # return core.convert_to_jewish(h_date).day
        return 14  # Tijdelijke testwaarde (Dag 14 van Nissan = Erev Pesach)
