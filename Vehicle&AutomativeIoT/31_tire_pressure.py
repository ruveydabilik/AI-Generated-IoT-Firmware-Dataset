import json

def process_input(data):
    """
    Processes incoming IoT sensor data for tire pressure monitoring.

    Expected JSON format:
    {
        "sensor_id": "FL_01",
        "pressure_kpa": 220.5,
        "temperature_c": 25.0,
        "battery_v": 3.1
    }
    """
    # Safety Thresholds (Standard Passenger Vehicle)
    MIN_PSI = 30.0
    MAX_PSI = 36.0
    CRITICAL_TEMP_C = 70.0
    LOW_BATTERY_V = 2.4

    try:
        # Parse the incoming JSON string
        reading = json.loads(data)

        sensor_id = reading.get("sensor_id", "Unknown")
        raw_pressure = reading.get("pressure_kpa", 0)
        temp_c = reading.get("temperature_c", 0)
        battery = reading.get("battery_v", 0)

        # Convert kPa to PSI
        # Equation: P_psi = P_kpa * 0.145038
        pressure_psi = round(raw_pressure * 0.145038, 2)

        # Initialize status flags
        status = "Normal"
        alerts = []

        # Logic Checks
        if pressure_psi < MIN_PSI:
            status = "Warning"
            alerts.append("Under-inflated")
        elif pressure_psi > MAX_PSI:
            status = "Warning"
            alerts.append("Over-inflated")
        if temp_c > CRITICAL_TEMP_C:
            status = "Critical"
            alerts.append("High Temperature")

        if battery < LOW_BATTERY_V:
            alerts.append("Low Sensor Battery")

        # Construct the response payload
        response = {
            "sensor": sensor_id,
            "display_value": f"{pressure_psi} PSI",
            "temperature": f"{temp_c}°C",
            "status": status,
            "alerts": alerts if alerts else ["None"],
            "system_ready": True
        }

        return json.dumps(response)

    except (ValueError, KeyError, TypeError) as e:
        return json.dumps({
            "status": "Error",
            "message": f"Invalid data format: {str(e)}",
            "system_ready": False
        })
