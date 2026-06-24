import json
import os

def process_input(data):
    """
    Processes incoming JSON data to store Wi-Fi credentials.
    Expected format: '{"ssid": "Your_Network", "password": "Your_Password"}'
    """
    STORAGE_FILE = "wifi_creds.json"

    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        # Validate required fields
        ssid = payload.get("ssid")
        password = payload.get("password")

        if not ssid or not password:
            return {"status": "error", "message": "Missing SSID or Password"}

        # Prepare the credential object
        creds = {
            "ssid": ssid,
            "password": password
        }

        # Write to local storage (Flash memory on most IoT boards)
        with open(STORAGE_FILE, "w") as f:
            json.dump(creds, f)

        return {
            "status": "success",
            "message": f"Credentials for '{ssid}' saved successfully."
        }

    except ValueError:
        return {"status": "error", "message": "Invalid JSON format"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

