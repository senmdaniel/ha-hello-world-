// We gebruiken het lokale bestand zodat alles 100% offline werkt
import { KosherZmanim } from "./kosher-zmanim.js";

export function berekenAlles(vandaag) {
  try {
    // 1. CONFIG (Gelijk aan load_config() uit uw Python-code)
    const config = {
      city: "Antwerp",
      timezone: "Europe/Brussels",
      latitude: 51.2194,
      longitude: 4.4025,
      elevation: 0
    };

    const opties = {
      date: vandaag,
      timeZoneId: config.timezone,
      latitude: config.latitude,
      longitude: config.longitude,
      elevation: config.elevation
    };

    // 2. BEREKEN BASE ZMANIM (Gelijk aan calculate_zmanim in Python)
    const complexZmanim = KosherZmanim.getZmanimJson(opties);
    const zmanimData = complexZmanim.zmanim;

    // 3. HEBREW DATE (Gelijk aan get_hebrew_date uit uw Python-code)
    // We initialiseren de Joodse kalender van KosherZmanim voor de huidige dag
    const joodseKalender = new KosherZmanim.JewishCalendar(vandaag);
    
    const hebrew = {
      hebrew_date_formatted: joodseKalender.toString(), // Bijv. "5 Sivan 5786"
      hebrew_month: joodseKalender.getJewishMonth(),    // Numerieke maand
      hebrew_day: joodseKalender.getJewishDayOfMonth(), // Dag van de maand
      hebrew_year: joodseKalender.getJewishYear(),      // Joods jaartal
      is_shabbos: joodseKalender.getDayOfWeek() === 7
    };

    // 4. EVENT SAFE (Gelijk aan get_event uit uw Python-code)
    let event = "0";
    const yomTovIndex = joodseKalender.getYomTovIndex();
    
    // Als er een feestdag of speciale herdenking is, halen we de naam op
    if (yomTovIndex !== -1 && yomTovIndex !== null) {
      event = joodseKalender.getYomTovName();
    }

    // 5. CUSTOM CALCULATION (Uw specifieke Pi/Loxone-berekeningen)
    const shkiasTijd = new Date(zmanimData.Sunset);
    const candleLighting = new Date(shkiasTijd.getTime() - (18 * 60 * 1000)); // 18 min vóór zonsondergang
    const tzeis85 = KosherZmanim.getTzeis8Point5Degrees(opties);              // Tzeis op 8.5 graden

    // 6. RESPONSE (Exact de mappenstructuur en velden die uw Python-API uitspuugde!)
    return {
      status: "ok",
      date: vandaag.toISOString(),
      hebrew: hebrew,
      event: event,
      zmanim: {
        alos_hashachar: formatteerTijd(zmanimData.AlosHashachar),
        netz_hachamah_sunrise: formatteerTijd(zmanimData.Sunrise),
        sof_zman_krias_shema_mga: formatteerTijd(zmanimData.SofZmanShmaMGA),
        sof_zman_krias_shema_gra: formatteerTijd(zmanimData.SofZmanShmaGRA),
        sof_zman_tefilah_gra: formatteerTijd(zmanimData.SofZmanTfilaGRA),
        chatzos_midday: formatteerTijd(zmanimData.Chatzos),
        mincha_gedolah: formatteerTijd(zmanimData.MinchaGedolah),
        mincha_ketanah: formatteerTijd(zmanimData.MinchaKetana),
        plag_hamincha: formatteerTijd(zmanimData.PlagHamincha),
        shkias_hachamah_sunset: formatteerTijd(shkiasTijd),
        candle_lighting: candleLighting.toLocaleTimeString('nl-NL', { hour: '2-digit', minute: '2-digit' }),
        tzeis_hakochavim_8_5_deg: tzeis85 ? new Date(tzeis85).toLocaleTimeString('nl-NL', { hour: '2-digit', minute: '2-digit' }) : formatteerTijd(zmanimData.Tzeis)
      },
      location: {
        city: config.city,
        timezone: config.timezone,
        latitude: config.latitude,
        longitude: config.longitude
      }
    };

  } catch (error) {
    // Vangt fouten op net als de 'except Exception as e' uit uw Python-code
    return {
      status: "error",
      error: error.message
    };
  }
}

// Hulpfunctie om ISO-tijdstrings om te zetten naar een schone digitale kloktijd (HH:MM)
function formatteerTijd(isoString) {
  if (!isoString) return "--:--";
  return new Date(isoString).toLocaleTimeString('nl-NL', { hour: '2-digit', minute: '2-digit' });
}
