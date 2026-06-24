import json

def process_input(data):
    """
    Processes incoming sensor data and triggers an alarm if the
    heart rate exceeds the safety threshold.
    """
    # Define our 'danger zone' threshold
    HEART_RATE_THRESHOLD = 100

    try:
        # Parse the JSON-formatted input
        # Assuming format: {"heart_rate": 85, "device_id": "sensor_01"}
        payload = json.loads(data)
        heart_rate = payload.get("heart_rate")
        device_id = payload.get("device_id", "Unknown Device")

        if heart_rate is None:
            return f"Error: Missing 'heart_rate' key in data from {device_id}."

        # Logic to trigger the alarm
        if heart_rate > HEART_RATE_THRESHOLD:
            # In a real scenario, this is where we'd toggle a GPIO pin
            # or send a push notification to a mobile app.
            alarm_status = {
                "status": "ALARM_TRIGGERED",
                "message": f"CRITICAL: Heart rate of {heart_rate} bpm detected on {device_id}!",
                "alert_level": "High"
            }
        else:
            alarm_status = {
                "status": "NORMAL",
                "message": f"Heart rate of {heart_rate} bpm is within safe limits.",
                "alert_level": "None"
            }

        return json.dumps(alarm_status)

    except json.JSONDecodeError:
        return "Error: Invalid JSON format received."
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

# --- Quick Test Case ---
# raw_json_input = '{"heart_rate": 115, "device_id": "ESP32_Wearable_01"}'
# print(process_input(raw_json_input))