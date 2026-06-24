import json

# Simulated persistent storage for users
# In a real IoT device, this would be loaded from a file or EEPROM
user_db = {
    "admin": {"pin": "1234", "role": "admin"},
    "guest": {"pin": "0000", "role": "user"}
}

def process_input(data):
    """
    Processes incoming JSON data to manage users on the IoT device.
    Supported actions: 'add', 'authenticate', 'remove'
    """
    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        action = payload.get("action")
        username = payload.get("username")
        pin = payload.get("pin")
        role = payload.get("role", "user")  # Default to 'user' if not specified

        # 1. Authenticate a User (e.g., for door access)
        if action == "authenticate":
            if username in user_db and user_db[username]["pin"] == pin:
                return json.dumps({"status": "success", "message": f"Access granted for {username}", "role": user_db[username]["role"]})
            else:
                return json.dumps({"status": "error", "message": "Invalid credentials"})

        # 2. Add a New User (Admin only logic can be added here)
        elif action == "add":
            if username in user_db:
                return json.dumps({"status": "error", "message": "User already exists"})

            user_db[username] = {"pin": pin, "role": role}
            return json.dumps({"status": "success", "message": f"User {username} added successfully"})

        # 3. Remove a User
        elif action == "remove":
            if username in user_db:
                del user_db[username]
                return json.dumps({"status": "success", "message": f"User {username} removed"})
            else:
                return json.dumps({"status": "error", "message": "User not found"})
         # 4. Unknown Action
        else:
            return json.dumps({"status": "error", "message": "Unknown action requested"})

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
