from datetime import date
from convertdate import hebrew
import homeassistant.util.dt as dt_util

class DateProvider:
    """Levert de juiste burgerlijke en Joodse datum aan de sensoren."""

    def __init__(self):
        pass

    def get_current_date(self) -> date:
        """Haalt de huidige lokale datum van Home Assistant op."""
        return dt_util.now().date()

    def get_hebrew_date_dict(self):
        """Converteert de huidige HA datum naar de Joodse kalender."""
        gregorian_date = self.get_current_date()
        h_year, h_month, h_day = hebrew.from_gregorian(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        )
        return {
            "hebrew_year": h_year,
            "hebrew_month": h_month,
            "hebrew_day": h_day
        }

    def get_current_jewish_month(self) -> int:
        """Geeft het nummer van de huidige Joodse maand terug."""
        return self.get_hebrew_date_dict()["hebrew_month"]

    def get_current_jewish_day(self) -> int:
        """Geeft het nummer van de huidige Joodse dag terug."""
        return self.get_hebrew_date_dict()["hebrew_day"]

    def get_jewish_date_string(self) -> str:
        """Maakt een mooie tekst van de Joodse datum voor de sensor."""
        data = self.get_hebrew_date_dict()
        # Maandenlijst om het nummer om te zetten in een naam
        maanden = [
            "Nisan", "Iyar", "Sivan", "Tammuz", "Av", "Elul",
            "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shevat", 
            "Adar", "Adar II"
        ]
        
        try:
            maand_naam = maanden[data["hebrew_month"] - 1]
        except IndexError:
            maand_naam = "Onbekend"
            
        return f"{data['hebrew_day']} {maand_naam} {data['hebrew_year']}"
