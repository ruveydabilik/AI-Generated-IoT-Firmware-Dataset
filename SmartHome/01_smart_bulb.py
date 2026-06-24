import json

class SmartBulb:
    def __init__(self, pin):
        self.pin = pin
        self.state = False

    def on(self):
        self.state = True
        print(f"[Hardware] GPIO {self.pin} set to HIGH. Bulb is ON.")

    def off(self):
        self.state = False
        print(f"[Hardware] GPIO {self.pin} set to LOW. Bulb is OFF.")

my_bulb = SmartBulb(pin=2)

def process_input(data):

    try:
        payload = json.loads(data)

        command = payload.get("command")
        value = payload.get("value", "").lower()

        if command == "power":

            if value == "on":
                my_bulb.on()
                return json.dumps({"status":"success"})

            elif value == "off":
                my_bulb.off()
                return json.dumps({"status":"success"})

            else:
                return json.dumps({"status":"error"})

        else:
            return json.dumps({"status":"error"})

    except Exception as e:
        raise