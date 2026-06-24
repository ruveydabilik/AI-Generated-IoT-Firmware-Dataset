import json

def process_input(data):
    """
    Processes sensor telemetry to detect driver fatigue.

    Expected JSON schema:
    {
        "ear": float,        # Eye Aspect Ratio (typically 0.2 - 0.3)
        "head_tilt": float,   # Degrees of forward tilt
        "is_yawning": bool,   # Boolean flag from vision shim
        "timestamp": int
    }
    """
    # Configuration Thresholds
    EAR_THRESHOLD = 0.21       # Eyes are considered closed below this
    TILT_THRESHOLD = 30.0      # Degrees (head nodding forward)

    try:
        # Parse the incoming JSON
        telemetry = json.loads(data) if isinstance(data, str) else data

        ear = telemetry.get("ear", 1.0)
        tilt = telemetry.get("head_tilt", 0)
        yawning = telemetry.get("is_yawning", False)

        # Initialize response
        status = "NORMAL"
        alert_level = 0  # 0: Safe, 1: Warning, 2: Critical
        action_required = False

        # 1. Check for Microsleep / Closed Eyes
        if ear < EAR_THRESHOLD:
            status = "DROWSINESS_DETECTED"
            alert_level = 2
            action_required = True

        # 2. Check for Head Slumping (IMU data)
        elif abs(tilt) > TILT_THRESHOLD:
            status = "HEAD_TILT_WARNING"
            alert_level = 1
            action_required = True

        # 3. Check for Excessive Yawning
        elif yawning:
            status = "FATIGUE_WARNING"
            alert_level = 1
            action_required = False # Log only, or minor chirp

        # Construct payload for the local actuator (buzzer/LED) or cloud log
        response = {
            "status": status,
            "alert_level": alert_level,
            "trigger_alarm": action_required,
            "metadata": {
                "ear_val": ear,
                "tilt_val": tilt
            }
        }

        return json.dumps(response)

    except (ValueError, KeyError, TypeError) as e:
        return json.dumps({"error": "Invalid input format", "details": str(e)})

# Example Usage:
# raw_data = '{"ear": 0.18, "head_tilt": 35, "is_yawning": false}'
# print(process_input(raw_data))
