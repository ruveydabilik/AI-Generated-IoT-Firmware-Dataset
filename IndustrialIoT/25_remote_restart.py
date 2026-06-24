import json
import os

def process_input(data):
    """
    Parses incoming JSON data and triggers a system restart if
    the correct command is received.
    """
    try:
        # Load the JSON string into a dictionary
        payload = json.loads(data)

        # We're looking for a specific key-value pair to prevent accidental triggers
        # Example input: {"command": "system_restart", "confirm": true}
        if payload.get("command") == "system_restart" and payload.get("confirm") is True:

            # For standard Linux IoT devices:
            # We use 'sudo reboot' to ensure the system shuts down and restarts correctly.
            #os.system('sudo reboot')

            return {
                "status": "initiating",
                "message": "Restart command accepted. Device is rebooting."
            }

        return {
            "status": "ignored",
            "message": "Invalid command or confirmation missing."
        }

    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "Malformed JSON input."
        }
    except Exception as e:
        # Catch-all for unexpected issues (like permission errors)
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }
