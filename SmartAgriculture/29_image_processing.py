import json
import base64

def process_input(data):
    """
    Processes incoming field imagery for crop health analysis.
    Expected JSON keys: 'image_b64', 'altitude', 'coords'.
    """

    try:
        # 1. Parse incoming JSON
        payload = json.loads(data)

        image_b64 = payload.get("image_b64", "")
        altitude = payload.get("altitude", 0)
        coords = payload.get("coords", [0, 0])

        # 2. Decode image bytes
        image_bytes = base64.b64decode(image_b64)

        # Simulated image metrics
        image_size = len(image_bytes)

        # Mock health analysis
        average_health = (image_size % 100) / 100.0
        stress_zones = image_size % 500

        # 3. Prepare telemetry
        result = {
            "status": "success",
            "telemetry": {
                "lat_long": coords,
                "alt_m": altitude
            },
            "analysis": {
                "avg_health_index": round(average_health, 4),
                "stress_pixel_count": stress_zones,
                "action_required":
                    "high" if average_health < 0.1 else "none"
            }
        }

        return json.dumps(result)

    except Exception as e:
        return json.dumps({
            "status": "critical_failure",
            "error": str(e)
        })