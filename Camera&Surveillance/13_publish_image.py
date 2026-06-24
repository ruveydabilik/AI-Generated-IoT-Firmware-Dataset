import base64
import json
import time

# Safe import for OpenCV
try:
    import cv2
except ImportError:
    cv2 = None


# --- Minimal mock for environments without camera/OpenCV ---
if cv2 is None:

    class DummyCapture:

        def isOpened(self):
            return True

        def read(self):
            return True, b"fake_frame"

        def release(self):
            pass


    class DummyCV2:

        IMWRITE_JPEG_QUALITY = 1

        def VideoCapture(self, *_):
            return DummyCapture()

        def imencode(self, *args, **kwargs):
            return True, b"fake_jpeg_data"

    cv2 = DummyCV2()


def process_input(data):
    """
    IoT Firmware Logic: Captures an image, encodes it, and prepares
    it for web transmission based on JSON commands.
    """

    try:
        # Parse the incoming JSON command
        # Expected format:
        # {"command": "capture", "device_id": "cam_01", "quality": 80}

        params = json.loads(data)

        if params.get("command") != "capture":
            return json.dumps({
                "status": "error",
                "message": "Invalid command"
            })

        # Initialize the camera
        camera = cv2.VideoCapture(0)

        # Give the sensor a split second to settle
        time.sleep(0.1)

        success, frame = camera.read()

        if not success:
            camera.release()

            return json.dumps({
                "status": "error",
                "message": "Failed to access camera"
            })

        # Downsample/compress image
        quality = params.get("quality", 75)

        encode_param = [
            int(cv2.IMWRITE_JPEG_QUALITY),
            quality
        ]

        # Encode to JPEG
        _, buffer = cv2.imencode('.jpg', frame, encode_param)

        # Convert to Base64
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Cleanup
        camera.release()

         # Prepare response
        response = {
            "status": "success",
            "device_id": params.get("device_id"),
            "timestamp": time.time(),
            "image_data": f"data:image/jpeg;base64,{jpg_as_text}"
        }

        return json.dumps(response)

    except Exception as e:

        return json.dumps({
            "status": "error",
            "message": str(e)
        })


# --- Quick Test Loop ---
if __name__ == "__main__":

    mock_request = json.dumps({
        "command": "capture",
        "device_id": "iot-edge-01",
        "quality": 85
    })

    print("Capturing and processing...")

    result = process_input(mock_request)

    print(f"Payload generated: {result[:100]}...")

