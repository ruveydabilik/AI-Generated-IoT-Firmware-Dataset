import json
import time

def process_input(data):
    """
    Parses incoming JSON data and triggers an SOS routine if
    emergency conditions are met.
    """
    try:
        # Parse the JSON string into a dictionary
        payload = json.loads(data)

        # Extract fields with safe defaults
        event_type = payload.get("event_type", "normal")
        battery_level = payload.get("battery", 100)
        location = payload.get("gps_coords", "Unknown")

        # Check for SOS trigger
        # We assume 'emergency' or 'sos' signals a crisis
        if event_type.lower() in ["sos", "emergency"]:
            return send_sos_alert(location, battery_level)

        else:
            print(f"[Info] Heartbeat received. Battery at {battery_level}%.")
            return False

    except json.JSONDecodeError:
        print("[Error] Invalid JSON format received.")
        return False
    except Exception as e:
        print(f"[Error] Unexpected firmware glitch: {e}")
        return False

def send_sos_alert(coords, battery):
    """
    Simulates the transmission of an SOS message via MQTT/HTTP.
    """
    print("\n--- EMERGENCY PROTOCOL ACTIVATED ---")
    print(f"[*] Dispatching SOS Signal...")
    print(f"[*] Location: {coords}")
    print(f"[*] Device Battery: {battery}%")
    print("[*] Alerting Emergency Contacts via Gateway...")
    print("-------------------------------------\n")
    return True

# --- Example Usage for Testing ---
# mock_json = '{"event_type": "SOS", "battery": 42, "gps_coords": "40.7128 N, 74.0060 W"}'
# process_input(mock_json)