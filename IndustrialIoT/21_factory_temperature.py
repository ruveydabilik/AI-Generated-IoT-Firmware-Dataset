import json

def process_input(data):
    """
    Processes incoming JSON data from factory temperature sensors.

    Expected JSON format:
    {
        "sensor_id": "TEMP_01",
        "temperature": 45.5,
        "unit": "C"
    }
    """
    # Thresholds for industrial safety
    THRESHOLD_WARNING = 75.0  # Celsius
    THRESHOLD_CRITICAL = 90.0 # Celsius

    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        sensor_id = payload.get("sensor_id", "UNKNOWN_DEVICE")
        temp = payload.get("temperature")

        # Basic validation
        if temp is None:
            return {"error": "Missing temperature value", "status": 400}

        # Logic for monitoring status
        status = "NORMAL"
        action = "NONE"

        if temp >= THRESHOLD_CRITICAL:
            status = "CRITICAL"
            action = "SHUTDOWN_IMMEDIATE"
        elif temp >= THRESHOLD_WARNING:
            status = "WARNING"
            action = "ACTIVATE_COOLING"
        elif temp < 0:
            status = "LOW_TEMP_ALERT"
            action = "CHECK_INSULATION"
        
        # Constructing the telemetry response
        result = {
            "device": sensor_id,
            "reading": f"{temp}°C",
            "status": status,
            "action_taken": action
        }

        # Log to "serial console" (stdout) for debugging
        print(f"[IOT-LOG] {sensor_id} reported {temp}°C. Status: {status}")

        return result

    except json.JSONDecodeError:
        return {"error": "Invalid JSON format", "status": 400}
    except Exception as e:
        return {"error": str(e), "status": 500}

