import json

def process_input(data):
    """
    Processes incoming UDP packets for an IoT device.
    Expects data to be a JSON-formatted string or byte-string.
    """
    try:
        # 1. Decode bytes to string if necessary (UDP standard)
        if isinstance(data, bytes):
            data = data.decode('utf-8')

        # 2. Parse JSON payload
        payload = json.loads(data)

        # 3. Extract core fields (with defaults to avoid KeyErrors)
        device_id = payload.get("device_id", "unknown_node")
        action = payload.get("action", "nop")
        params = payload.get("params", {})

        # 4. Route logic based on the 'action' key
        if action == "telemetry":
            # Example: {"action": "telemetry", "params": {"temp": 24.5}}
            temperature = params.get("temp")
            return f"ACK: Received telemetry from {device_id} (Temp: {temperature}°C)"

        elif action == "toggle_relay":
            # Example: {"action": "toggle_relay", "params": {"state": "on"}}
            state = params.get("state", "off")
            # In a real hackathon, you'd trigger a GPIO pin here
            return f"ACK: GPIO Relay on {device_id} set to {state}"

        elif action == "ping":
            return f"ACK: Pong from {device_id}"

        else:
            return f"ERR: Unknown action '{action}' from {device_id}"

    except json.JSONDecodeError:
        return "ERR: Malformed JSON packet"
    except Exception as e:
        return f"ERR: Unexpected processing error - {str(e)}"

