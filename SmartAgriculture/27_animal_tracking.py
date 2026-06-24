import json
import math

def process_input(data):
    """
    Processes incoming sensor data from the animal tracker.
    Input: JSON string containing lat, lon, pet_id, and battery_level.
    """
    # Define 'Home' coordinates (Geofence Center)
    HOME_LAT = 34.0522
    HOME_LON = -118.2437
    GEOFENCE_RADIUS_KM = 0.5  # 500 meters
    BATTERY_THRESHOLD = 20    # Alert at 20%

    try:
        # Parse the JSON input
        payload = json.loads(data)

        pet_id = payload.get("pet_id", "Unknown")
        current_lat = payload.get("lat")
        current_lon = payload.get("lon")
        battery = payload.get("battery_level", 100)

        if current_lat is None or current_lon is None:
            return {"status": "error", "message": "Missing GPS coordinates"}

        # --- Haversine Formula for Distance Calculation ---
        # Radius of Earth in kilometers
        R = 6371.0

        # Convert decimal degrees to radians
        phi1, phi2 = math.radians(HOME_LAT), math.radians(current_lat)
        delta_phi = math.radians(current_lat - HOME_LAT)
        delta_lambda = math.radians(current_lon - HOME_LON)

        # Calculate distance
        a = math.sin(delta_phi / 2)**2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2)**2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance_km = R * c

        # --- Logic Checks ---
        status_alerts = []
        is_safe = True

        # Check Geofence
        if distance_km > GEOFENCE_RADIUS_KM:
            status_alerts.append(f"ALERT: {pet_id} has left the safe zone!")
            is_safe = False

        # Check Battery
        if battery < BATTERY_THRESHOLD:
            status_alerts.append(f"WARNING: Low battery on {pet_id} ({battery}%)")

        # Prepare the response/log
        result = {
            "pet_id": pet_id,
            "distance_from_home_km": round(distance_km, 4),
            "is_safe": is_safe,
            "battery_ok": battery >= BATTERY_THRESHOLD,
            "alerts": status_alerts
        }

        return json.dumps(result)

    except (ValueError, TypeError) as e:
        return json.dumps({"status": "error", "message": f"Invalid data format: {str(e)}"})

# Example Usage:
# raw_json = '{"pet_id": "Rex_001", "lat": 34.0530, "lon": -118.2440, "battery_level": 15}'
# print(process_input(raw_json))
