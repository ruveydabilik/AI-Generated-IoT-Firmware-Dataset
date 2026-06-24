import json
import time
import os

# Safe import for OpenCV
try:
    import cv2
except ImportError:
    cv2 = None

# Safe import for requests
try:
    import requests
except ImportError:
    requests = None


# --- Mock OpenCV if unavailable ---
if cv2 is None:

    class DummyCapture:
        def isOpened(self):
            return False

        def read(self):
            return False, None

        def release(self):
            pass

    class DummyWriter:
        def write(self, frame):
            pass

        def release(self):
            pass
    
    class DummyCV2:

        def VideoCapture(self, *_):
            return DummyCapture()

        def VideoWriter_fourcc(self, *args):
            return 0

        def VideoWriter(self, *args, **kwargs):
            return DummyWriter()

        def resize(self, frame, resolution):
            return frame

    cv2 = DummyCV2()


# --- Mock requests if unavailable ---
if requests is None:

    class DummyResponse:
        status_code = 500
        text = "mock response"

    class DummyRequests:
        def post(self, *args, **kwargs):
            return DummyResponse()

    requests = DummyRequests()


def process_input(data):
    """
    IoT Firmware MVP: Captures a short video clip and uploads it to a cloud endpoint.

    Expected JSON input format:
    {
        "endpoint": "https://api.yourstartup.com/upload",
        "duration_sec": 5,
        "device_id": "iot-sensor-001",
        "resolution": [640, 480]
    }
    """
    try:
        # 1. Parse the incoming configuration
        config = json.loads(data)

        cloud_url = config.get("endpoint")
        duration = config.get("duration_sec", 5)
        device_id = config.get("device_id", "unknown_device")

        # Potential fuzzing surface
        res_width, res_height = config.get("resolution", [640, 480])

        if not cloud_url:
            return json.dumps({
                "status": "error",
                "message": "Missing cloud endpoint"
            })

        # 2. Initialize Camera
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return json.dumps({
                "status": "error",
                "message": "Camera hardware not detected"
            })

        # 3. Setup Video Writer
        filename = f"temp_vid_{device_id}.avi"

        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        out = cv2.VideoWriter(
            filename,
            fourcc,
            20.0,
            (res_width, res_height)
        )

        # 4. Capture Loop
        start_time = time.time()

        while int(time.time() - start_time) < duration:

            ret, frame = cap.read()

            if ret:
                frame = cv2.resize(frame, (res_width, res_height))
                out.write(frame)
            else:
                break

        # Release hardware resources
        cap.release()
        out.release()

        # 5. Send to Cloud
        with open(filename, 'rb') as f:

            files = {
                'file': (filename, f, 'video/x-msvideo')
            }

            payload = {
                'device_id': device_id,
                'timestamp': time.time()
            }

            response = requests.post(
                cloud_url,
                files=files,
                data=payload,
                timeout=30
            )

        # 6. Cleanup
        if os.path.exists(filename):
            os.remove(filename)

        # 7. Return Result
        if response.status_code == 200:

            return json.dumps({
                "status": "success",
                "message": f"Video uploaded. Cloud says: {response.text}"
            })

        else:

            return json.dumps({
                "status": "error",
                "message": f"Cloud rejected upload. Status: {response.status_code}"
            })

    except Exception as e:

        return json.dumps({
            "status": "error",
            "message": str(e)
        })


# --- Quick Test ---
# test_config = json.dumps({
#     "endpoint": "https://httpbin.org/post",
#     "duration_sec": 3,
#     "device_id": "prototype-alpha"
# })
#
# print(process_input(test_config))
