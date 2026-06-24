import json
import os

def process_input(data):
    """
    Parses JSON input to identify and read a configuration file.

    Args:
        data (str): A JSON-formatted string containing the 'config_file' path.

    Returns:
        dict: The parsed configuration data or an error message.
    """
    try:
        # Step 1: Parse the incoming command/data
        # We're expecting something like: '{"config_file": "settings.json"}'
        input_json = json.loads(data)

        # Get the filename from the input, default to 'config.json' if not specified
        filename = input_json.get("config_file", "config.json")

        # Step 2: Check if the file actually exists before we try to open it
        if not os.path.exists(filename):
            return {
                "status": "error",
                "message": f"Configuration file '{filename}' not found."
            }

        # Step 3: Read and parse the config file
        with open(filename, 'r') as f:
            config_data = json.load(f)

        return {
            "status": "success",
            "data": config_data
        }

    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid JSON format in input data."
        }
    except Exception as e:
        # Catch-all for those weird I/O errors that happen in the field
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }

# --- Example Usage ---
# command = '{"config_file": "sensor_config.json"}'
# result = process_input(command)
# print(result)
