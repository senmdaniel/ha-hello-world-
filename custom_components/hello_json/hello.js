// We kopiëren de officiële Home Assistant Dashboard-structuur
import { LitElement, html, css } from "https://unpkg.com";

class PiZmanimCard extends LitElement {
  static get properties() {
    return {
      _hass: {},
      _config: {},
      _data: { type: Object }
    };
  }

  constructor() {
    super();
    this._data = null;
    // Haal direct de live JSON-data op van de Raspberry Pi
    this.haalPiDataOp();
  }

  haalPiDataOp() {
    fetch('http://192.168.178')
      .then(response => response.json())
      .then(json => {
        this._data = json;
      })
      .catch(err => console.error("Fout bij ophalen Pi-data:", err));
  }

  setConfig(config) {
    this._config = config;
  }

  // Dit zorgt ervoor dat de JSON puur en netjes in de browser wordt geprint
  render() {
    if (!this._data) {
      return html`<pre>Data van de Pi wordt geladen...</pre>`;
    }
    return html`
      <pre style="white-space: pre-wrap; word-wrap: break-word; font-family: monospace;">
        ${JSON.stringify(this._data, null, 2)}
      </pre>
    `;
  }
}

// Registreer de kaart officieel in Home Assistant zoals button-card dat doet
customElements.define('pi-zmanim-card', PiZmanimCard);
