import json

# Mock hardware classes for non-MicroPython environments
try:
    from machine import Pin, PWM

except ImportError:

    class Pin:
        OUT = 0

        def __init__(self, pin, *args, **kwargs):
            self.pin = pin

    class PWM:
        def __init__(self, pin, freq=1000, *args, **kwargs):
            self.pin = pin
            self.frequency = freq
            self.current_duty = 0

        def duty(self, value):
            self.current_duty = value
            print(f"[Mock PWM] Pin {self.pin.pin} duty set to {value}")


# Initialize the LED on Pin 2 with a frequency of 1000Hz
led_pwm = PWM(Pin(2), freq=1000)

def process_input(data):
    """
    Parses JSON input from a mobile app and adjusts LED brightness.
    Expected format: {"brightness": 0-100}
    """
    try:
        # Parse the incoming JSON string
        payload = json.loads(data)

        # Extract brightness value (default to 0 if missing)
        brightness_percent = payload.get("brightness", 0)

        # Constrain input to 0-100 range
        brightness_percent = max(0, min(100, brightness_percent))

        # Convert 0-100% to 10-bit duty cycle (0-1023)
        duty_cycle = int((brightness_percent / 100) * 1023)

        # Apply the new brightness
        led_pwm.duty(duty_cycle)

        return {"status": "success", "level": brightness_percent}

    except (ValueError, KeyError, TypeError) as e:
        # Return error details for debugging the app's requests
        return {"status": "error", "message": str(e)}

# Example Usage:
# request_from_app = '{"brightness": 75}'
# print(process_input(request_from_app))