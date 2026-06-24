import json
import time

# Mocking GPIO for demonstration; in production, use: import RPi.GPIO as GPIO
try:
    import RPi.GPIO as GPIO
except ImportError:
    # Fallback for testing environments without GPIO pins
    class MockGPIO:
        BCM = OUT = LOW = HIGH = None
        def setmode(self, mode): pass
        def setup(self, pin, mode): pass
        def output(self, pin, state): print(f"[Hardware] Pin {pin} set to {state}")
        def cleanup(self): pass
    GPIO = MockGPIO()

# Hardware Configuration (Pin BCM Numbers)
PIN_IGNITION = 17  # Connects to Ignition Relay
PIN_STARTER = 27   # Connects to Starter Motor Relay
SECRET_KEY = "DEV_AUTH_7721"  # Replace with a secure token

# Initializing Hardware
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_IGNITION, GPIO.OUT)
GPIO.setup(PIN_STARTER, GPIO.OUT)

def process_input(data):
    """
    Processes incoming JSON commands to control vehicle ignition and starter.
    Expects format: {"action": "start/stop", "key": "string", "safety_check": bool}
    """
    try:
        # Parse the JSON input
        payload = json.loads(data)
        action = payload.get("action")
        provided_key = payload.get("key")
        safety_clear = payload.get("safety_check", False)

        # 1. Authentication Check
        if provided_key != SECRET_KEY:
            return json.dumps({"status": "error", "message": "Unauthorized access."})

        # 2. Logic for Starting the Vehicle
        if action == "start":
            if not safety_clear:
                return json.dumps({"status": "error", "message": "Safety sensors not cleared."})
            
            print("Initiating Start Sequence...")

            # Step A: Engage Ignition (Turn on electronics/fuel pump)
            GPIO.output(PIN_IGNITION, True)
            #time.sleep(1.5)  # Wait for fuel system to prime

            # Step B: Engage Starter
            GPIO.output(PIN_STARTER, True)
            #time.sleep(2.0)  # Crank the engine for 2 seconds
            GPIO.output(PIN_STARTER, False)

            return json.dumps({"status": "success", "message": "Vehicle started."})

        # 3. Logic for Stopping the Vehicle
        elif action == "stop":
            print("Shutting down engine...")
            # Kill Ignition to stop the engine
            GPIO.output(PIN_IGNITION, False)
            GPIO.output(PIN_STARTER, False)
            return json.dumps({"status": "success", "message": "Vehicle stopped."})

        else:
            return json.dumps({"status": "error", "message": "Invalid action."})

    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# --- Example Usage ---
# command = '{"action": "start", "key": "DEV_AUTH_7721", "safety_check": true}'
# response = process_input(command)
# print(response)
