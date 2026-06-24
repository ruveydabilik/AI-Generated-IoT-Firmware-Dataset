import json

def process_input(data):
    """
    Processes humidity data to control a ventilation fan.

    Expected JSON format:
    {
        "humidity": 68.5,
        "current_state": "OFF"
    }
    """
    # Configuration thresholds
    THRESHOLD_HIGH = 65.0  # Turn fan ON
    THRESHOLD_LOW = 55.0   # Turn fan OFF

    try:
        # Parse the incoming JSON data
        payload = json.loads(data)
        humidity = payload.get("humidity")
        current_state = payload.get("current_state", "OFF").upper()

        if humidity is None:
            return {"error": "Missing humidity value", "action": "STAY"}

        # Logic with Hysteresis:
        # 1. If humidity is high and fan is off -> Turn it on.
        # 2. If fan is on, keep it on until humidity drops below the low threshold.

        if humidity > THRESHOLD_HIGH and current_state == "OFF":
            action = "FAN_ON"
            reason = f"Humidity ({humidity}%) exceeded {THRESHOLD_HIGH}%"
        elif humidity < THRESHOLD_LOW and current_state == "ON":
            action = "FAN_OFF"
            reason = f"Humidity ({humidity}%) dropped below {THRESHOLD_LOW}%"
        else:
            action = "STAY"
            reason = "Threshold not met or state already optimal"

        return {
            "action": action,
            "current_humidity": humidity,
            "message": reason
        }
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format", "action": "STAY"}
    except Exception as e:
        return {"error": str(e), "action": "STAY"}

# --- Quick Test ---
# sample_data = '{"humidity": 72.0, "current_state": "OFF"}'
# print(process_input(sample_data))