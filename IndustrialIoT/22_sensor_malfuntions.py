import json

def process_input(data):
    """
    Processes incoming JSON data from IoT sensors and flags malfunctions.

    Expected JSON format:
    {
        "sensor_id": "DHT22_01",
        "type": "temperature",
        "value": 24.5,
        "unit": "C"
    }
    """
    # Define physical constraints for our prototype
    # Anything outside these is likely a hardware failure or a short circuit
    SENSOR_CONFIGS = {
        "temperature": {"min": -40.0, "max": 85.0, "unit": "C"},
        "humidity": {"min": 0.0, "max": 100.0, "unit": "%"},
        "pressure": {"min": 300.0, "max": 1100.0, "unit": "hPa"}
    }

    try:
        # 1. Parse the incoming telemetry
        payload = json.loads(data)

        sensor_id = payload.get("sensor_id", "UNKNOWN_DEVICE")
        sensor_type = payload.get("type")
        reading = payload.get("value")

        # 2. Check for Missing Data (Flatline/Null Malfunction)
        if reading is None:
            return {
                "id": sensor_id,
                "status": "MALFUNCTION",
                "reason": "NULL_READING",
                "msg": "Sensor returned no value. Check wiring/power."
            }

        # 3. Validate Sensor Type
        if sensor_type not in SENSOR_CONFIGS:
            return {
                "id": sensor_id,
                "status": "ERROR",
                "reason": "UNSUPPORTED_TYPE",
                "msg": f"Sensor type '{sensor_type}' is not configured."
            }
        
         # 4. Out-of-Bounds Detection (Saturation or Short Circuit)
        limits = SENSOR_CONFIGS[sensor_type]
        if reading < limits["min"] or reading > limits["max"]:
            return {
                "id": sensor_id,
                "status": "MALFUNCTION",
                "reason": "OUT_OF_BOUNDS",
                "value": reading,
                "msg": f"Reading {reading} is outside physical limits [{limits['min']}, {limits['max']}]."
            }

        # 5. All checks passed
        return {
            "id": sensor_id,
            "status": "OK",
            "value": reading,
            "msg": "Telemetry validated successfully."
        }

    except json.JSONDecodeError:
        return {"status": "ERROR", "reason": "CORRUPT_JSON", "msg": "Failed to parse JSON string."}
    except Exception as e:
        return {"status": "CRITICAL", "reason": "UNEXPECTED_FAILURE", "msg": str(e)}

# --- Quick Test Cases ---
# Normal: '{"sensor_id": "T1", "type": "temperature", "value": 22.5}'
# Malfunction: '{"sensor_id": "T1", "type": "temperature", "value": 999.9}'
# Failure: '{"sensor_id": "H1", "type": "humidity", "value": null}'
