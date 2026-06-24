import json

# Simulating a local device state (e.g., a smart thermostat or light)
device_state = {
    "power": "OFF",
    "brightness": 75,
    "temp_threshold": 22.5,
    "last_sync": "2026-05-13T10:00:00Z"
}

def process_input(data):
    """
    Processes JSON-formatted input from the mobile app to
    synchronize device state and settings.
    """
    global device_state

    try:
        # Parse the incoming JSON
        payload = json.loads(data)
        action = payload.get("action")

        # 1. Action: APP_SYNC_REQUEST (App wants the latest device data)
        if action == "GET_STATUS":
            return json.dumps({
                "status": "success",
                "device_state": device_state,
                "message": "State synchronized to mobile app."
            })

        # 2. Action: UPDATE_STATE (App is changing a setting)
        elif action == "UPDATE_STATE":
            new_params = payload.get("params", {})

            # Update internal state with new values from the app
            for key in new_params:
                if key in device_state:
                    device_state[key] = new_params[key]

            # In a real project, this is where you'd trigger
            # physical hardware changes (GPIO pins, PWM, etc.)
            return json.dumps({
                "status": "success",
                "updated_keys": list(new_params.keys()),
                "message": "Device state updated successfully."
            })
        
         # 3. Action: FIRMWARE_RESET (Generic maintenance command)
        elif action == "RESET":
            # Logic for a soft reboot or factory reset
            return json.dumps({"status": "success", "message": "Rebooting..."})

        else:
            return json.dumps({
                "status": "error",
                "message": f"Unknown action: {action}"
            })

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# --- Example Usage for your testing ---
# incoming_json = '{"action": "UPDATE_STATE", "params": {"power": "ON", "brightness": 90}}'
# print(process_input(incoming_json))
