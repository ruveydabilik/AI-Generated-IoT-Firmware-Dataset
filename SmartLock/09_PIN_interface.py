import json

def process_input(data):
    """
    Processes incoming JSON data to manage PIN state changes.
    Expected JSON format: {"pin_id": 12, "state": "HIGH", "mode": "output"}
    """
    try:
        # 1. Parse the incoming JSON string
        command = json.loads(data)

        # 2. Extract our variables with defaults to prevent crashing
        pin_id = command.get("pin_id")
        target_state = command.get("state")
        mode = command.get("mode", "output")

        # 3. Validation: Make sure we actually have a pin to talk to
        if pin_id is None:
            return json.dumps({"status": "error", "message": "No pin_id provided"})

        # 4. Interface Logic
        # In a real IoT device, you'd do something like:
        # pin = machine.Pin(pin_id, machine.Pin.OUT)
        # pin.value(1 if target_state == "HIGH" else 0)

        print(f"[FIRMWARE] Configuring PIN {pin_id} as {mode}...")
        print(f"[FIRMWARE] Setting PIN {pin_id} to {target_state}.")

        # 5. Return a confirmation response
        response = {
            "status": "success",
            "pin_affected": pin_id,
            "new_state": target_state,
            "message": f"Interface for PIN {pin_id} updated successfully."
        }
        return json.dumps(response)

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON string received"})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Unexpected error: {str(e)}"})

# Example Usage:
# incoming_json = '{"pin_id": 14, "state": "HIGH", "mode": "output"}'
# print(process_input(incoming_json))