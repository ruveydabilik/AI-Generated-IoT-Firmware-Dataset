import json
import math

# Project: IoT Sleep Monitor Firmware
# Student ID: 2026-IOT-404
# Note: Ensure the accelerometer is calibrated before deployment!

def process_input(data):
    """
    Processes JSON sensor data to determine sleep states.
    Expected JSON format: {"accel_x": 0.1, "accel_y": 0.02, "accel_z": 0.98, "hr": 65}
    """
    try:
        # Parse the incoming JSON
        reading = json.loads(data)

        # Extract variables with default fallbacks
        x = reading.get("accel_x", 0)
        y = reading.get("accel_y", 0)
        z = reading.get("accel_z", 0)
        hr = reading.get("hr", 70)  # Heart rate in BPM

        # 1. Calculate Movement Magnitude (Vector Sum)
        # Using the formula: $M = \sqrt{x^2 + y^2 + z^2}$
        magnitude = math.sqrt(x**2 + y**2 + z**2)

        # 2. Normalize (subtracting 1g of gravity)
        # We want the "jerk" or movement delta, not the gravity vector
        movement_delta = abs(magnitude - 1.0)

        # 3. Simple Heuristic Sleep Logic
        # These thresholds are experimental based on common actigraphy standards
        if movement_delta > 0.15:
            state = "Awake / Restless"
            quality_score = 20
        elif 0.05 < movement_delta <= 0.15:
            state = "Light Sleep"
            quality_score = 60
        else:
            # Low movement + lower heart rate usually indicates Deep Sleep
            if hr < 60:
                state = "Deep Sleep"
                quality_score = 100
            else:
                state = "Quiet Wakefulness/REM"
                quality_score = 80
         # Return the analysis as a dictionary (ready for MQTT or logging)
        return {
            "status": "success",
            "sleep_state": state,
            "movement_intensity": round(movement_delta, 4),
            "heart_rate": hr,
            "quality_index": quality_score
        }

    except (ValueError, TypeError, KeyError) as e:
        return {
            "status": "error",
            "message": f"Invalid data format: {str(e)}"
        }

# Example Usage (for testing the project):
# sample_data = '{"accel_x": 0.01, "accel_y": 0.01, "accel_z": 1.01, "hr": 55}'
# print(process_input(sample_data))
