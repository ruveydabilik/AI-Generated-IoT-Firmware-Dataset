import sqlite3
import json

def process_input(data):
    """
    Parses JSON input and persists it to a local SQLite database.
    Designed for lightweight IoT firmware environments.
    """
    try:
        # 1. Parse the incoming JSON string
        payload = json.loads(data)

        # Extracting values (with fallbacks to prevent KeyErrors)
        user_id = payload.get("user_id", "unknown_user")
        value = payload.get("value", 0.0)

        # 2. Connect to (or create) the local database file
        # In IoT, we often store this on the SD card or internal flash
        conn = sqlite3.connect('iot_storage.db')
        cursor = conn.cursor()

        # 3. Create the table if it doesn't exist yet
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                value REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 4. Insert the data safely using parameter substitution
        # (This prevents SQL injection, even in small projects!)
        cursor.execute('''
            INSERT INTO user_data (user_id, value)
            VALUES (?, ?)
        ''', (user_id, value))

        # 5. Commit changes and close the connection
        conn.commit()
        conn.close()

        print(f"Successfully logged data for: {user_id}")
        return True
    
    except json.JSONDecodeError:
        print("Error: Invalid JSON format received.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return False

