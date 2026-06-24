import json
import hashlib
import time

# Mocking the device's current state
CURRENT_VERSION = "1.0.4"
STORAGE_PATH = "/tmp/firmware_update.bin"

def process_input(data):
    """
    Processes incoming JSON commands to manage the camera firmware update lifecycle.
    Expected actions: 'check_update', 'download_firmware', 'apply_update'
    """
    try:
        # Parse the JSON input
        request = json.loads(data)
        action = request.get("action")
        payload = request.get("payload", {})

        print(f"[System] Received action: {action}")

        if action == "check_update":
            new_version = payload.get("version")
            if new_version > CURRENT_VERSION:
                return json.dumps({
                    "status": "update_available",
                    "current": CURRENT_VERSION,
                    "available": new_version,
                    "size_mb": payload.get("size_mb")
                })
            else:
                return json.dumps({"status": "up_to_date", "version": CURRENT_VERSION})

        elif action == "download_firmware":
            url = payload.get("url")
            expected_checksum = payload.get("checksum")

            print(f"[Network] Downloading from {url}...")
            # Simulation of download delay
            #time.sleep(1)

            # Simulated binary data for the firmware
            simulated_content = b"firmware_binary_data_v1.0.5"

            # Verify Integrity (SHA-256)
            actual_checksum = hashlib.sha256(simulated_content).hexdigest()

            if actual_checksum == expected_checksum:
                with open(STORAGE_PATH, "wb") as f:
                    f.write(simulated_content)
                return json.dumps({"status": "download_complete", "checksum_verified": True})
            else:
                return json.dumps({"status": "error", "message": "Checksum mismatch. File corrupted."})

        elif action == "apply_update":
            print("[System] Commencing flash process. Do not power off...")
            # Simulate hardware flashing
            #time.sleep(2)

            # In a real scenario, we would trigger a bootloader flag and reboot
            return json.dumps({
                "status": "success",
                "message": "Firmware applied. Rebooting...",
                "new_version": payload.get("version")
            })

        else:
            return json.dumps({"status": "error", "message": "Unknown action"})

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# --- Example Usage ---
# update_request = json.dumps({
#     "action": "download_firmware",
#     "payload": {
#         "url": "https://api.iotstartup.com/v1/dist/cam_v1.0.5.bin",
#         "checksum": "5ec363162594a10f824905f42c67672957b98f2479e00192e21b0e515d481b49"
#     }
# })
# print(process_input(update_request))

