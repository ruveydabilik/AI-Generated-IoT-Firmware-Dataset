import json

def process_input(data):
    """
    Processes incoming sensor data to detect potential collisions.

    Expected JSON format:
    {
        "distance_cm": float,
        "velocity_ms": float (optional),
        "sensor_id": string
    }
    """
    try:
        # Parse the JSON string into a dictionary
        telemetry = json.loads(data)

        # Extract variables with sensible defaults
        distance = telemetry.get("distance_cm", float('inf'))
        velocity = telemetry.get("velocity_ms", 0.0)
        sensor_id = telemetry.get("sensor_id", "unknown_unit")

        # Configuration Constants (Tunable for specific hardware)
        CRITICAL_ZONE = 15.0  # cm
        WARNING_ZONE = 45.0   # cm
        TIME_TO_COLLISION_LIMIT = 0.5  # seconds

        # Initialize response state
        status = "CLEAR"
        action = "PROCEED"
        alert_level = 0

        # Logic 1: Static Distance Check
        if distance <= CRITICAL_ZONE:
            status = "IMMINENT_COLLISION"
            action = "EMERGENCY_BRAKE"
            alert_level = 2
        elif distance <= WARNING_ZONE:
            status = "CAUTION_NEARBY_OBJECT"
            action = "REDUCE_SPEED"
            alert_level = 1

        # Logic 2: Dynamic Velocity Check (Time-to-Collision)
        # Formula: TTC = distance / velocity
        # Only calculate if moving toward the object (positive velocity)

        if velocity > 0:
            # Convert distance to meters for SI consistency: $d_{m} = \frac{d_{cm}}{100}$
            dist_m = distance / 100.0
            ttc = dist_m / velocity

            if ttc <= TIME_TO_COLLISION_LIMIT:
                status = "VELOCITY_HAZARD"
                action = "EMERGENCY_BRAKE"
                alert_level = 2

        # Construct the output payload
        result = {
            "sensor_id": sensor_id,
            "status": status,
            "action": action,
            "alert_level": alert_level,
            "metrics": {
                "current_dist": distance,
                "closing_speed": velocity
            }
        }

        return json.dumps(result)

    except (json.JSONDecodeError, TypeError, ZeroDivisionError) as e:
        return json.dumps({
            "status": "ERROR",
            "message": f"Invalid telemetry stream: {str(e)}"
        })
