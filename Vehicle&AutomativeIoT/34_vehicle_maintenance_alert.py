import json

def process_input(data):
    """
    Processes vehicle telemetry to generate maintenance alerts.

    Expected JSON keys:
    - mileage: current odometer reading (int/float)
    - last_oil_change: mileage at last service (int/float)
    - battery_voltage: current battery level (float)
    - coolant_temp: engine temperature in Celsius (int/float)
    """
    try:
        # Parse the incoming JSON string
        telemetry = json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return {"status": "error", "message": "Invalid JSON format"}

    alerts = []

    # 1. Oil Life Monitoring
    # Standard interval: 7,500 miles/km
    mileage = telemetry.get("mileage", 0)
    last_oil_change = telemetry.get("last_oil_change", 0)

    if (mileage - last_oil_change) >= 7500:
        alerts.append("MAINTENANCE_REQUIRED: Oil change overdue.")
    elif (mileage - last_oil_change) >= 7000:
        alerts.append("REMINDER: Oil change due soon.")

    # 2. Battery Health Check
    # A healthy car battery sits at ~12.6V; below 11.8V is a critical starting risk.
    battery_v = telemetry.get("battery_voltage", 12.6)
    if battery_v < 11.8:
        alerts.append(f"CRITICAL: Low battery voltage ({battery_v}V). Risk of no-start.")
    elif battery_v < 12.2:
        alerts.append(f"WARNING: Weak battery detected ({battery_v}V).")

    # 3. Engine Health (Overheating)
    # Normal operating temp is usually 90°C to 104°C.
    temp = telemetry.get("coolant_temp", 90)
    if temp > 110:
        alerts.append(f"EMERGENCY: Engine overheating! ({temp}°C)")
    elif temp > 105:
        alerts.append(f"WARNING: High engine temperature detected ({temp}°C).")

    # Final response construction
    return {
        "status": "success",
        "alerts_found": len(alerts),
        "notifications": alerts,
        "timestamp_processed": "2026-05-13T23:44:00Z" # Example timestamp
    }

# Example usage for testing:
# raw_data = '{"mileage": 55000, "last_oil_change": 47000, "battery_voltage": 11.5, "coolant_temp": 112}'
# print(process_input(raw_data))
