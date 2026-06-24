import json
import base64

def process_input(data):
    """
    Processes incoming IoT sensor/camera data to detect pests.

    Args:
        data (str): JSON-formatted string containing 'image_raw' (base64),
                   'device_id', and 'sensitivity'.
    Returns:
        str: JSON-formatted response with detection results and action status.
    """
    try:
        # Parse the incoming JSON
        request_payload = json.loads(data)

        device_id = request_payload.get("device_id", "edge-node-01")
        image_raw = request_payload.get("image_raw", "")
        sensitivity = request_payload.get("sensitivity", 0.5)

        if not image_raw:
            return json.dumps({"status": "error", "message": "No image data provided."})

        # 1. Decode the image (for processing by your CV library)
        # In a real scenario, you'd pass this to OpenCV or PIL
        image_bytes = base64.b64decode(image_raw)

        # 2. Detection Logic Placeholder
        # This is where your model (e.g., MobileNet or a custom TFLite model) would run.
        # Let's simulate a detection result.
        detected_pests = []

        # MOCK DETECTION LOGIC:
        # Let's assume our model found something.
        # In production, this comes from: model.predict(image_bytes)
        mock_inference_results = [
            {"label": "rodent", "confidence": 0.88},
            {"label": "spider", "confidence": 0.42}
        ]

        for detection in mock_inference_results:
            if detection["confidence"] >= sensitivity:
                detected_pests.append(detection["label"])

        # 3. Decision Tree
        pest_found = len(detected_pests) > 0
        action_taken = "none"

        if pest_found:
            # Here you'd trigger a GPIO pin to flash an LED,
            # sound a buzzer, or send a notification to your phone.
            action_taken = "triggered_deterrent_and_notify"

        # 4. Prepare the response
        response = {
            "device_id": device_id,
            "pest_detected": pest_found,
            "detected_species": detected_pests,
            "action_status": action_taken,
            "log_id": "log_" + str(hash(image_raw[:20])) # Quick unique ID
        }

        return json.dumps(response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Firmware processing failed: {str(e)}"
        })
