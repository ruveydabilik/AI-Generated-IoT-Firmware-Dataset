import json

def process_input(data):
    """
    Processes incoming IoT sensor data and determines the state
    of the irrigation valve based on rain detection.
    """
    try:
        # Parse the incoming JSON-formatted string
        payload = json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return {"error": "Invalid JSON input"}

    # Extract current sensor states
    # Defaulting to 'True' for rain is a "fail-safe" approach
    is_raining = payload.get("rain_detected", True)

    # Check if the system is currently trying to water
    valve_requested = payload.get("valve_requested", False)

    # Logic: Irrigation only runs if requested AND it's not raining
    if is_raining:
        valve_state = False
        message = "Rain detected: Irrigation inhibited."
    else:
        valve_state = valve_requested
        message = "No rain: Following schedule."

    # Return the command payload for the actuator
    return {
        "valve_open": valve_state,
        "system_msg": message
    }
