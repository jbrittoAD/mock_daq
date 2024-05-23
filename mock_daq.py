import time
import threading

class MockDAQDevice:
    def __init__(self):
        self.pins = {}
        self.toggled_pins = {}

    def configure_digital_channel(self, pin, direction):
        self.pins[pin] = {
            'direction': direction,
            'state': False
        }

    def write_digital_pin(self, pin, state):
        if pin in self.pins and self.pins[pin]['direction'] == 'output':
            self.pins[pin]['state'] = state
        else:
            raise ValueError("Pin not configured as output or does not exist.")

    def read_digital_pin(self, pin):
        if pin in self.pins and self.pins[pin]['direction'] == 'input':
            return self.pins[pin]['state']
        else:
            raise ValueError("Pin not configured as input or does not exist.")

    def toggle_pin(self, pin, interval=1):
        if pin not in self.pins:
            raise ValueError("Pin does not exist.")
        if self.pins[pin]['direction'] != 'input':
            raise ValueError("Pin is not configured as input.")

        def toggle():
            while True:
                current_state = self.read_digital_pin(pin)
                self.pins[pin]['state'] = not current_state
                self.toggled_pins[pin] = self.pins[pin]['state']
                time.sleep(interval)

        thread = threading.Thread(target=toggle)
        thread.daemon = True
        thread.start()
