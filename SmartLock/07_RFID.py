import json

# Simulating a simple database of authorized RFID UIDs
# In a production environment, this might be stored in a protected file or synced via API
AUTHORIZED_USERS = {
    "A1:B2:C3:D4": "Alice (Admin)",
    "E5:F6:G7:H8": "Bob (Engineer)",
    "09:10:11:12": "Charlie (Guest)"
}

def process_input(data):
    """
    Processes incoming JSON data from the RFID reader and
    authenticates the user based on their UID.
    """
    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        # Extract the UID (Universal Identifier) from the RFID card
        card_uid = payload.get("uid")
        device_id = payload.get("device_id", "Unknown-Node")

        if not card_uid:
            return json.dumps({"status": "error", "message": "No UID provided"})

        print(f"[Device: {device_id}] Scanning card: {card_uid}...")

        # Authentication Logic
        if card_uid in AUTHORIZED_USERS:
            user_name = AUTHORIZED_USERS[card_uid]
            print(f"✅ Access Granted: Welcome, {user_name}!")

            # Here is where you'd trigger your GPIO pins to unlock a door
            # set_gpio(RELAY_PIN, HIGH)

            return json.dumps({
                "status": "success",
                "authorized": True,
                "user": user_name
            })
        else:
            print("❌ Access Denied: Unauthorized Card.")

            # Maybe trigger a red LED or a buzzer
            # set_gpio(BUZZER_PIN, HIGH)

            return json.dumps({
                "status": "denied",
                "authorized": False,
                "user": None
            })

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# --- Quick Test ---
if __name__ == "__main__":
    # Example of data coming from the hardware sensor
    test_input = '{"uid": "A1:B2:C3:D4", "device_id": "Front-Door-Reader"}'
    result = process_input(test_input)
    print(f"Response to MCU: {result}")
