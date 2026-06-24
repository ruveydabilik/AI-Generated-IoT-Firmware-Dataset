import json

def process_input(data):
    """
    Processes JSON input to control the emergency siren hardware.

    Expected JSON format:
    {
        "command": "test_siren" | "activate" | "silence",
        "duration_ms": 5000,
        "intensity": 0.8
    }
    """
    try:
        # Parse the input data
        payload = json.loads(data)
        command = payload.get("command")

        # Hardware simulation / Logic mapping
        if command == "test_siren":
            duration = payload.get("duration_ms", 1000)
            return {
                "status": "success",
                "action": f"Performing {duration}ms chirp test.",
                "siren_active": True
            }

        elif command == "activate":
            intensity = payload.get("intensity", 1.0)
            return {
                "status": "warning",
                "action": f"FULL ACTIVATION at {intensity * 100}% volume.",
                "siren_active": True
            }

        elif command == "silence":
            return {
                "status": "success",
                "action": "Siren deactivated.",
                "siren_active": False
            }
        
        else:
            return {
                "status": "error",
                "message": f"Unknown command: {command}"
            }

    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON format."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Quick Test ---
# test_json = '{"command": "test_siren", "duration_ms": 2000}'
# print(process_input(test_json))
