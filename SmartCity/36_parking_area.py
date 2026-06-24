import json

def process_input(data):
    """
    Parses sensor telemetry to assess parking spot occupancy.

    Expected JSON format:
    {
        "sensor_id": "SN-782",
        "distance_cm": 45,
        "battery_level": 88,
        "timestamp": 1715678512
    }
    """
    # Configuration: Distance threshold (cm) to trigger an 'Occupied' state
    # If a car is parked, the sensor distance will be much shorter than the floor.
    OCCUPANCY_THRESHOLD = 150

    try:
        # Load data if it's a string; otherwise assume it's already a dict
        payload = json.loads(data) if isinstance(data, str) else data

        sensor_id = payload.get("sensor_id", "Unknown")
        distance = payload.get("distance_cm", 0)
        battery = payload.get("battery_level", 0)

        # Core Logic: Occupancy Assessment
        # We assume 0 is a sensor error, so we filter for positive values
        is_occupied = 0 < distance < OCCUPANCY_THRESHOLD

        # Construct the outbound message for the gateway/cloud
        processed_state = {
            "dev_id": sensor_id,
            "occupied": is_occupied,
            "meta": {
                "reading": distance,
                "battery_low": battery < 15,
                "unit": "cm"
            }
        }

        return json.dumps(processed_state)

    except (json.JSONDecodeError, TypeError, AttributeError) as e:
        # Return a structured error so the gateway knows the payload was junk
        return json.dumps({
            "error": "Malformed JSON or Invalid Data Type",
            "details": str(e)
        })

# --- Example Usage ---
raw_payload = '{"sensor_id": "SPOT-042", "distance_cm": 42, "battery_level": 92}'
print(process_input(raw_payload))
