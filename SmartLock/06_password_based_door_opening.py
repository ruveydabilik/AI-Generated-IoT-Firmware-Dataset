import json

# Simulated hardware states
DOOR_LOCKED = True
SECRET_PASSWORD = "OpenSesame123"

def process_input(data):
    """
    Processes incoming JSON data to control a door lock.
    Expected JSON format: {"password": "your_password_here"}
    """
    global DOOR_LOCKED

    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        # Validate that the 'password' key exists
        if "password" not in payload:
            return json.dumps({
                "status": "error",
                "message": "Missing password field"
            })

        user_attempt = payload["password"]

        # Authentication Logic
        if user_attempt == SECRET_PASSWORD:
            DOOR_LOCKED = False
            # In a real IoT app, you'd trigger a GPIO pin here:
            # gpio.write(RELAY_PIN, HIGH)

            return json.dumps({
                "status": "success",
                "door_state": "unlocked",
                "message": "Access granted. Welcome home!"
            })
        else:
            return json.dumps({
                "status": "denied",
                "door_state": "locked",
                "message": "Incorrect password. Security alerted."
            })
    except json.JSONDecodeError:
        return json.dumps({
            "status": "error",
            "message": "Invalid JSON format"
        })

# --- Example Usage ---
# incoming_json = '{"password": "OpenSesame123"}'
# print(process_input(incoming_json))