import json

# Mocking hardware interaction for the MVP
# In production, we'd use something like RPi.GPIO or a specific camera lib
def set_ir_leds(state: bool):
    status = "ON" if state else "OFF"
    print(f"[HARDWARE] Infrared LEDs toggled: {status}")

def set_ir_cut_filter(active: bool):
    status = "ENGAGED" if active else "DISENGAGED"
    print(f"[HARDWARE] IR-Cut Filter (Daylight filter): {status}")

def process_input(data):
    """
    Processes incoming JSON data to control Night Vision Mode.
    Expected format: {"command": "set_night_vision", "enabled": true}
    """
    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        # Guard clause for the correct command
        if payload.get("command") != "set_night_vision":
            return json.dumps({"status": "error", "message": "Invalid command"})

        # Get the desired state
        enable_mode = payload.get("enabled", False)

        if enable_mode:
            # 1. Disable IR-cut filter (allows IR light to hit the sensor)
            set_ir_cut_filter(False)
            # 2. Fire up the IR LEDs
            set_ir_leds(True)
            result_msg = "Night vision activated."
        else:
            # 1. Engage IR-cut filter (blocks IR for natural daylight colors)
            set_ir_cut_filter(True)
            # 2. Turn off IR LEDs to save power
            set_ir_leds(False)
            result_msg = "Night vision deactivated."

        return json.dumps({
            "status": "success",
            "night_vision": "on" if enable_mode else "off",
            "message": result_msg
        })
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Malformed JSON input"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# --- Quick Test ---
if __name__ == "__main__":
    # Simulate a request from the mobile app/dashboard
    test_input = '{"command": "set_night_vision", "enabled": true}'
    print(f"Server response: {process_input(test_input)}")
