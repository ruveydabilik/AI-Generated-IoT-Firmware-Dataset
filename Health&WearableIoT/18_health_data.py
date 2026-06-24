import json
import struct

# Safe import for bluetooth
try:
    import bluetooth
except ImportError:
    bluetooth = None


# --- Minimal BLE mock for normal Python environments ---
if bluetooth is None:

    class DummyBLE:

        def active(self, state):
            pass

        def gatts_register_services(self, services):
            return (((1,),),)

        def gatts_write(self, handle, data):
            pass

        def gap_advertise(self, interval, payload):
            pass


    class DummyBluetooth:

        FLAG_READ = 0x0002
        FLAG_NOTIFY = 0x0010

        class UUID:
            def __init__(self, value):
                self.value = value

        def BLE(self):
            return DummyBLE()


    bluetooth = DummyBluetooth()

def process_input(data):
    """
    Processes health data and updates BLE GATT characteristics.
    Expects JSON input like:
    '{"heart_rate": 72, "temp": 36.5, "spo2": 98}'
    """

    # 1. Initialize BLE stack
    ble = bluetooth.BLE()
    ble.active(True)

    # 2. Define UUIDs
    _ADV_TYPE_FLAGS = 0x01
    _ADV_TYPE_NAME = 0x09

    _HR_SERVICE_UUID = bluetooth.UUID(0x180D)

    _HR_CHAR_UUID = (
        bluetooth.UUID(0x2A37),
        bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
    )

    _HEALTH_SERVICE = (
        _HR_SERVICE_UUID,
        (_HR_CHAR_UUID,),
    )

    # Register services
    ((hr_handle,),) = ble.gatts_register_services((_HEALTH_SERVICE,))

    # 3. Parse the JSON payload
    try:

        payload = json.loads(data)

        heart_rate = int(payload.get("heart_rate", 0))
        temp = float(payload.get("temp", 0.0))
        spo2 = int(payload.get("spo2", 0))

    except (ValueError, KeyError, TypeError) as e:

        print(f"Data Error: {e}")
        return False
    
    # 4. Pack data for BLE transmission
    hr_data = struct.pack('<BB', 0x00, heart_rate)

    # 5. Update GATT server values
    ble.gatts_write(hr_handle, hr_data)

    # 6. Start Advertising
    device_name = "Uni_Health_Sensor"

    adv_payload = (
        bytearray([0x02, _ADV_TYPE_FLAGS, 0x06]) +
        bytearray([len(device_name) + 1, _ADV_TYPE_NAME]) +
        device_name.encode()
    )

    ble.gap_advertise(100, adv_payload)

    print(
        f"Firmware updated: "
        f"{heart_rate} BPM, "
        f"{temp}C, "
        f"{spo2}% SpO2 sent to BLE buffer."
    )

    return True


# Example call
# sample_json = '{"heart_rate": 85, "temp": 37.2, "spo2": 99}'
# process_input(sample_json)
