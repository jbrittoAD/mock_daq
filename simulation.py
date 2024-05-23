import time
from mock_daq import MockDAQDevice

def print_pin_state(device, pin):
    state = device.read_digital_pin(pin)
    timestamp = time.time()
    print(f"[{timestamp:.6f}] State of {pin}: {'HIGH' if state else 'LOW'}")
    return state

def test_blinking(device, pin, interval, duration):
    print(f"Starting blink test for {pin} with interval {interval}s for {duration}s.")

    # Start blinking
    start_time = time.time()
    device.start_blink_pin(pin, interval)
    print(f"[{start_time:.6f}] Started blinking {pin} every {interval} seconds.")

    time.sleep(duration)

    # Stop blinking
    stop_time = time.time()
    device.stop_blink_pin(pin)
    print(f"[{stop_time:.6f}] Stopped blinking {pin}.")

    print(f"Blink test for {pin} with interval {interval}s completed.")

def main():
    # Create an instance of MockDAQDevice
    device = MockDAQDevice()
    print("Device initialized.")

    # Configure pin 'pin1' as input
    device.configure_digital_channel('pin1', 'input')
    print("Configured pin1 as input.")

    # Define test parameters
    intervals = [0.5, 1, 2]  # Different intervals for blinking
    test_duration = 5  # Duration for each test

    for interval in intervals:
        test_blinking(device, 'pin1', interval, test_duration)

if __name__ == '__main__':
    main()
