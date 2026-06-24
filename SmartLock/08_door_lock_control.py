import json

def process_input(data):
    """
    Processes incoming JSON data over Bluetooth to control a door lock.

    Expected JSON format:
    {
        "command": "unlock",
        "secret_key": "admin123"
    }
    """
    # A simple hardcoded key for our beginner project
    MASTER_KEY = "open-sesame-123"

    try:
        # Step 1: Parse the incoming JSON string
        payload = json.loads(data)

        # Step 2: Extract details
        command = payload.get("command", "").lower()
        provided_key = payload.get("secret_key", "")

        # Step 3: Validation and Hardware Control logic
        if provided_key != MASTER_KEY:
            return json.dumps({"status": "error", "message": "Unauthorized: Invalid Key"})

        if command == "unlock":
            # Simulate GPIO High to trigger the solenoid/motor
            print("[HARDWARE] Signal Sent: UNLOCKING DOOR...")
            return json.dumps({"status": "success", "message": "Door Unlocked"})

        elif command == "lock":
            # Simulate GPIO Low
            print("[HARDWARE] Signal Sent: LOCKING DOOR...")
            return json.dumps({"status": "success", "message": "Door Locked"})

        else:
            return json.dumps({"status": "error", "message": "Unknown Command"})

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format"})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Unexpected error: {str(e)}"})
    
# --- Example Usage ---
# incoming_bluetooth_data = '{"command": "unlock", "secret_key": "open-sesame-123"}'
# response = process_input(incoming_bluetooth_data)
# print(f"Response to Mobile App: {response}")