import json

def process_input(data):
    """
    Processes sensor data for a Smart Street Lamp.

    Expected JSON input:
    {
        "ambient_light": float (0-100, where 0 is pitch black),
        "motion_detected": bool,
        "manual_override": bool (optional)
    }
    """
    try:
        # Parse the incoming JSON data
        payload = json.loads(data)

        # Extract sensor values with default fallbacks
        light_level = payload.get("ambient_light", 100)
        motion = payload.get("motion_detected", False)
        override = payload.get("manual_override", False)

        # Configuration Thresholds
        LUX_THRESHOLD = 30.0  # Below this, we consider it "dark"

        # Logic Engine
        status = "OFF"
        brightness = 0

        if override:
            status = "MANUAL_ON"
            brightness = 100
        elif light_level < LUX_THRESHOLD:
            if motion:
                status = "ACTIVE_NIGHT"
                brightness = 100
            else:
                status = "STANDBY_NIGHT"
                brightness = 20
        else:
            status = "DAYLIGHT_OFF"
            brightness = 0

        # Construct the hardware response/state
        result = {
            "lamp_status": status,
            "led_pwm_level": brightness,
            "energy_saving_active": brightness < 100 and status != "DAYLIGHT_OFF",
            "telemetry": {
                "input_lux": light_level,
                "motion_trigger": motion
            }
        }

        return json.dumps(result, indent=2)

    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# --- Quick Test ---
sample_sensor_data = '{"ambient_light": 15.5, "motion_detected": true}'
print(process_input(sample_sensor_data))
