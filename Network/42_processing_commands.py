import json

def process_input(data):
    """
    Processes incoming JSON commands for an IoT device.
    Expected format: '{"command": "action_name", "value": 123}'
    """
    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        # Extract the command (default to None if missing)
        command = payload.get("command")
        params = payload.get("params", {}) # Optional extra data

        print(f"[IoT] Received command: {command}")

        # Command Dispatcher
        if command == "led_on":
            # Replace with actual GPIO logic, e.g., led.on()
            return {"status": "success", "message": "LED turned ON"}

        elif command == "led_off":
            # Replace with actual GPIO logic, e.g., led.off()
            return {"status": "success", "message": "LED turned OFF"}

        elif command == "set_temp":
            target_temp = params.get("target")
            return {"status": "success", "message": f"Temperature set to {target_temp}°C"}

        elif command == "get_status":
            return {
                "status": "online",
                "uptime": "12h 30m",
                "battery": "85%"
            }

        else:
            return {"status": "error", "message": f"Unknown command: {command}"}

    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON format"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Quick Test ---
if __name__ == "__main__":
    test_json = '{"command": "set_temp", "params": {"target": 22}}'
    response = process_input(test_json)
    print(f"Response: {response}")
