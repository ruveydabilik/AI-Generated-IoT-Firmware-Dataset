import json

def process_input(data):
    """
    Processes JSON input to calculate power and energy consumption.

    Expected JSON format:
    {
        "voltage_v": 120.0,
        "current_a": 1.5,
        "interval_s": 10
    }
    """
    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        # Extract values with default fallbacks to avoid NoneType errors
        v = payload.get("voltage_v", 0.0)
        i = payload.get("current_a", 0.0)
        t = payload.get("interval_s", 0)

        # 1. Calculate Instantaneous Power (Watts)
        # Formula: P = V * I
        power_w = v * i

        # 2. Calculate Energy Consumed (Watt-hours)
        # Formula: E = (P * t) / 3600
        # (We divide by 3600 to convert seconds to hours)
        energy_wh = (power_w * t) / 3600

        # Return the processed telemetry
        return json.dumps({
            "status": "online",
            "metrics": {
                "instantaneous_power_w": round(power_w, 2),
                "consumed_energy_wh": round(energy_wh, 6),
                "unit": "Wh"
            },
            "error": None
        })

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
    
# --- Quick Test Case ---
# raw_data = '{"voltage_v": 230, "current_a": 0.5, "interval_s": 3600}'
# print(process_input(raw_data))
