import json
import logging

# Configure basic logging for our MVP debugging
logging.basicConfig(level=logging.INFO)

def start_recording():
    """
    Placeholder for the hardware-specific recording trigger.
    In a production environment, this would interface with
    the camera module or a media server.
    """
    logging.info("ACTION: Motion detected! Starting video recording...")
    # Add hardware-specific code here (e.g., camera.start_recording())

def process_input(data):
    """
    Processes JSON-formatted sensor data and triggers recording
    if motion is detected.
    """
    try:
        # Parse the JSON string into a dictionary
        payload = json.loads(data)

        # Extract sensor type and value
        sensor_type = payload.get("sensor_type")
        motion_detected = payload.get("value", False)

        # Logic gate: trigger recording only if it's the motion sensor
        # and it returns a 'True' state.
        if sensor_type == "motion" and motion_detected:
            start_recording()
            return {"status": "success", "action": "recording_started"}

        return {"status": "idle", "action": "none"}

    except json.JSONDecodeError:
        logging.error("Failed to decode JSON data.")
        return {"status": "error", "message": "Invalid JSON format"}
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return {"status": "error", "message": str(e)}
    
# --- Quick Test Case ---
if __name__ == "__main__":
    sample_json = '{"sensor_type": "motion", "value": true}'
    process_input(sample_json)
