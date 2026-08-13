import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_energy_stats(entity_id="sensor.home_energy_power"):
    """Fetches current energy or power consumption data from Home Assistant or local smart meter API."""
    ha_url = os.getenv("HOME_ASSISTANT_URL", "http://192.168.8.26:8123/api")
    ha_token = os.getenv("HOME_ASSISTANT_TOKEN", "")

    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }

    try:
        url = f"{ha_url}/states/{entity_id}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            state = data.get("state")
            unit = data.get("attributes", {}).get("unit_of_measurement", "W")
            friendly_name = data.get("attributes", {}).get("friendly_name", entity_id)
            return f"Sensor: {friendly_name} | Current Value: {state} {unit}"
        else:
            return f"Error: Received status code {response.status_code} from Home Assistant."
            
    except Exception as e:
        return f"Error connecting to energy monitor: {str(e)}"
