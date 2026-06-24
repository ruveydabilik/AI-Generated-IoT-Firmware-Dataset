import json
import time

def process_input(data):
    """
    Processes incoming JSON telemetry data for a public transport vehicle.
    Handles validation, speed monitoring, and prepares data for server transmission.
    """
    try:
        # 1. Parse the incoming JSON string
        telemetry = json.loads(data)

        # 2. Required Field Validation
        required_fields = ['vehicle_id', 'latitude', 'longitude', 'speed']
        if not all(field in telemetry for field in required_fields):
            return {"status": "error", "message": "Missing required telemetry fields"}

        # 3. Extract and Sanitize Data
        v_id = telemetry.get('vehicle_id')
        lat = float(telemetry.get('latitude'))
        lon = float(telemetry.get('longitude'))
        speed = float(telemetry.get('speed'))
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

        # 4. Simple Edge Logic: Speed Alert
        # Example threshold: 80 km/h for urban transport
        alert_flag = False
        if speed > 80:
            alert_flag = True

        # 5. Geofence Check (Simplified)
        # Check if the vehicle is roughly within city limits (Example: NYC-ish)
        in_zone = (40.0 <= lat <= 41.0) and (-74.5 <= lon <= -73.5)

        # 6. Prepare Outbound Payload
        processed_payload = {
            "v_id": v_id,
            "ts": timestamp,
            "coords": [lat, lon],
            "spd": speed,
            "safety_alert": alert_flag,
            "in_service_area": in_zone,
            "status": "ready_for_uplink"
        }

        # In a real IoT scenario, you would trigger the MQTT/HTTP publish here.
        return json.dumps(processed_payload)

    except (ValueError, TypeError) as e:
        return json.dumps({"status": "error", "message": f"Invalid data format: {str(e)}"})

# --- Example Usage for Testing ---
# raw_data = '{"vehicle_id": "BUS-402", "latitude": 40.7128, "longitude": -74.0060, "speed": 45}'
# print(process_input(raw_data))
