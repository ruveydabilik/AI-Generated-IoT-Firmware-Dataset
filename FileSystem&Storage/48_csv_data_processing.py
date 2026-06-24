import json
import csv
import io

def process_input(data):
    """
    Parses a JSON object containing a CSV string and processes the records.
    Expected JSON format: {"device_id": "ESP32_01", "csv_payload": "timestamp,temp,hum\n17156900,22.5,45\n..."}
    """
    try:
        # 1. Decode the incoming JSON data
        # If it's already a dict, we skip the loading step
        payload = json.loads(data) if isinstance(data, str) else data

        # 2. Grab the CSV string from the 'csv_payload' key
        csv_string = payload.get("csv_payload", "")

        if not csv_string:
            return {"status": "error", "message": "No CSV data found in payload"}

        # 3. Use StringIO to simulate a file for the CSV reader
        # This is way better than manual string splitting!
        csv_file = io.StringIO(csv_string)
        reader = csv.DictReader(csv_file)

        processed_records = []

        for row in reader:
            # Example Processing: Clean up data or perform simple math
            # Let's say we want to ensure numbers are floats
            formatted_row = {}
            for key, value in row.items():
                try:
                    # Try to convert to float if it's a number
                    formatted_row[key] = float(value)
                except ValueError:
                    # Keep it as a string if it's a label (like 'status')
                    formatted_row[key] = value

            processed_records.append(formatted_row)

        return {
            "status": "success",
            "device": payload.get("device_id", "unknown"),
            "count": len(processed_records),
            "data": processed_records
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Example Usage ---
# raw_json = '{"device_id": "DHT22_Sensor", "csv_payload": "temp,hum\\n24.5,50\\n24.7,51"}'
# print(process_input(raw_json))
