import json
import time

# Simulation of non-volatile memory for persistent totals
# In a real ESP32/Raspberry Pi setup, you'd save this to a file or NVS
meter_state = {
    "cumulative_liters": 0.0,
    "last_pulse_time": time.time(),
    "leak_threshold": 30.0  # Liters per minute for anomaly detection
}

def process_input(data):
    """
    Processes incoming sensor data for a smart water meter.
    Expected JSON format: {"meter_id": "W-101", "pulses": 45, "duration_sec": 10}
    """
    global meter_state

    try:
        # Parse the incoming JSON
        payload = json.loads(data) if isinstance(data, str) else data

        meter_id = payload.get("meter_id", "unknown")
        pulses = payload.get("pulses", 0)
        duration = payload.get("duration_sec", 1)

        # 1. Conversion Logic
        # Standard calibration example: 450 pulses = 1 Liter
        # Formula: Volume = Pulses / K-Factor
        k_factor = 450.0
        liters_measured = pulses / k_factor

        # 2. Flow Rate Calculation
        # Flow Rate (L/min) = (Volume / Duration) * 60
        flow_rate_lpm = (liters_measured / duration) * 60

        # 3. Update Persistent State
        meter_state["cumulative_liters"] += liters_measured

        # 4. Anomaly/Leak Detection
        status = "NORMAL"
        if flow_rate_lpm > meter_state["leak_threshold"]:
            status = "ALARM_HIGH_FLOW"
        elif pulses > 0 and flow_rate_lpm < 0.1:
            status = "WARNING_DRIP_DETECTED"

        # 5. Prepare Outbound Telemetry
        telemetry = {
            "device_id": meter_id,
            "timestamp": time.time(),
            "flow_rate_lpm": round(flow_rate_lpm, 3),
            "total_volume_l": round(meter_state["cumulative_liters"], 3),
            "status": status,
            "health_check": "OK"
        }

        return json.dumps(telemetry)

    except (ValueError, KeyError, TypeError) as e:
        return json.dumps({"error": "Invalid payload", "details": str(e)})

# --- Quick Test ---
sample_data = '{"meter_id": "SENS-01", "pulses": 225, "duration_sec": 30}'
print(f"Processed Output: {process_input(sample_data)}")
