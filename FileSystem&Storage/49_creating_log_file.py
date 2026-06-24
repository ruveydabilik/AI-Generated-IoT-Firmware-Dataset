import json
import os

def process_input(data):
    """
    Parses JSON data and appends it to a local log file.
    Designed for IoT edge cases like corrupted JSON or missing files.
    """
    log_filename = "device_log.txt"

    try:
        # 1. Handle potential string input vs already parsed dict
        if isinstance(data, str):
            payload = json.loads(data)
        else:
            payload = data

        # 2. Extract a message or just use the whole object
        # In a real IoT setup, you'd usually want a timestamp here!
        log_entry = {
            "status": "LOG_EVENT",
            "payload": payload
        }

        # 3. Open file in 'append' mode ('a')
        # This creates the file if it doesn't exist
        with open(log_filename, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return {"status": "success", "message": "Data logged successfully."}

    except ValueError as e:
        # Catch JSON decoding errors (very common in flaky RF/Serial links)
        return {"status": "error", "message": f"Invalid JSON format: {e}"}

    except Exception as e:
        # Catch filesystem errors (like SD card being full or pulled out)
        return {"status": "error", "message": f"Filesystem error: {e}"}

# --- Quick Test ---
# raw_json = '{"sensor": "DHT22", "temp": 24.5, "humidity": 60}'
# print(process_input(raw_json))

