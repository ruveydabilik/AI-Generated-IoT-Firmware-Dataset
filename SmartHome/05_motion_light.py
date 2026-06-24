import json

def process_input(data):
    """
    Analyzes incoming sensor JSON data and toggles smart lighting
    based on motion detection events.
    """
    try:
        # Parse the incoming JSON string into a dictionary
        # Expected schema: {"sensor": "motion_01", "motion_detected": true}
        payload = json.loads(data)

        # Extract the motion status, defaulting to False if the key is missing
        is_motion_detected = payload.get("motion_detected", False)
        sensor_id = payload.get("sensor", "unknown_sensor")

        if is_motion_detected:
            # Logic to trigger the light
            # In a real-world scenario, this might be a GPIO write
            # or an HTTP POST to a smart bulb API.
            return trigger_light_action(sensor_id, "ON")

        return f"Status: Standby. No motion reported by {sensor_id}."

    except json.JSONDecodeError:
        return "Error: Received invalid JSON format."
    except Exception as e:
        return f"Error processing firmware logic: {str(e)}"

def trigger_light_action(source, state):
    """
    Simulates the physical hardware or network command to the light.
    """
    # Replace the print statement with actual hardware control code
    # e.g., smart_bulb.turn_on()
    print(f"[IOT_HUB] Command sent: Light {state} (Triggered by {source})")
    return f"Success: Light turned {state}."

# --- Example Usage ---
# input_json = '{"sensor": "hallway_pir", "motion_detected": true}'
# print(process_input(input_json))