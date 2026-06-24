import json
import time

# A mock database to keep track of our DIY network's state
network_registry = {
    "nodes": {},
    "thresholds": {
        "temperature": {"min": 15, "max": 30},
        "humidity": {"min": 30, "max": 70}
    }
}

def process_input(data):
    """
    Processes incoming JSON telemetry from WSN nodes.
    Expected format:
    {
        "node_id": "sensor_01",
        "battery": 85,
        "readings": {"temperature": 22.5, "humidity": 45}
    }
    """
    try:
        # Parse the JSON string into a dictionary
        payload = json.loads(data)

        node_id = payload.get("node_id")
        battery = payload.get("battery")
        readings = payload.get("readings", {})

        if not node_id:
            return {"status": "error", "message": "Missing node_id"}

        # Log the timestamp of the last communication
        network_registry["nodes"][node_id] = {
            "last_seen": time.time(),
            "battery_level": battery
        }

        alerts = []

         # Analyze sensor readings against our DIY thresholds
        for sensor, value in readings.items():
            limits = network_registry["thresholds"].get(sensor)
            if limits:
                if value < limits["min"]:
                    alerts.append(f"ALERT: {node_id} - {sensor} too low ({value})")
                elif value > limits["max"]:
                    alerts.append(f"ALERT: {node_id} - {sensor} too high ({value})")

        # Battery management: Because swapping AA batteries every week is no fun
        if battery and battery < 15:
            alerts.append(f"LOW BATTERY: {node_id} is at {battery}%")

        response = {
            "status": "success",
            "node_processed": node_id,
            "alerts_triggered": alerts
        }

        return json.dumps(response)

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# --- Example Usage ---
if __name__ == "__main__":
    # Simulating an incoming packet from a DHT22 sensor node
    incoming_data = '{"node_id": "living_room_01", "battery": 12, "readings": {"temperature": 32.5, "humidity": 40}}'

    result = process_input(incoming_data)
    print(result)

