import json
import os
from datetime import datetime

def process_input(data):
    """
    Processes incoming JSON data to log indoor temperature history.

    Expected JSON format:
    {
        "sensor_id": "living_room_01",
        "temperature": 22.5,
        "unit": "C"
    }
    """
    LOG_FILE = "temperature_history.jsonl"

    try:
        # Parse the incoming JSON string if it's not already a dict
        if isinstance(data, str):
            payload = json.loads(data)
        else:
            payload = data

        # Extract necessary fields
        sensor_id = payload.get("sensor_id", "unknown_sensor")
        temp = payload.get("temperature")
        unit = payload.get("unit", "C")

        if temp is None:
            return {"status": "error", "message": "Missing temperature value"}

        # Create the log entry with a server-side timestamp
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "sensor_id": sensor_id,
            "temperature": temp,
            "unit": unit
        }

        # Append to the log file
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        return {
            "status": "success",
            "message": f"Logged {temp}{unit} from {sensor_id}"
        }

    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON format"}
    except Exception as e:
        return {"status": "error", "message": str(e)}