import json

def process_input(data):
    """
    Processes JSON-formatted ZigBee data for a hackathon IoT demo.
    Expected schema: {"device_id": str, "type": str, "payload": dict}
    """
    try:
        # 1. Parse the incoming JSON string
        message = json.loads(data)

        device_id = message.get("device_id", "unknown")
        msg_type = message.get("type", "telemetry")  # e.g., 'telemetry' or 'status'
        payload = message.get("payload", {})

        print(f"[ZigBee Stack] Processing packet from {device_id}...")

        # 2. Logic Gateway: Handle different device behaviors
        # Example: Simple Temperature Sensor
        if "temperature" in payload:
            temp = payload["temperature"]
            print(f"-> Climate Update: {temp}°C")

            # Simple "Thermostat" logic for the demo
            if temp > 25:
                return json.dumps({
                    "target_device": "fan_actuator_01",
                    "command": "ON",
                    "status": "cooling_triggered"
                })

        # Example: Motion Sensor
        elif "occupancy" in payload:
            occupied = payload["occupancy"]
            state = "Active" if occupied else "Idle"
            print(f"-> Motion Update: {state}")

            return json.dumps({
                "target_device": device_id,
                "command": "ACK",
                "status": "received"
            })

        # 3. Default response for unhandled clusters/attributes
        return json.dumps({"status": "ignored", "reason": "no_matching_logic"})

    except json.JSONDecodeError:
        return json.dumps({"error": "invalid_json"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# --- Demo Usage ---
# raw_zigbee_json = '{"device_id": "sensor_th_99", "payload": {"temperature": 28.5}}'
# response = process_input(raw_zigbee_json)
# print(response)
