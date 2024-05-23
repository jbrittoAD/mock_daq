# test_mock_daq.py
import time
import pytest
from mock_daq import MockDAQDevice

@pytest.fixture
def device():
    """
    Fixture to create a MockDAQDevice instance with a configured input pin.

    This fixture creates a `MockDAQDevice` object, configures the pin named 'pin1' as an input,
    and returns the device instance for use in the tests.

    Returns:
        MockDAQDevice: An instance of the MockDAQDevice class.
    """
    device = MockDAQDevice()
    device.configure_digital_channel('pin1', 'input')
    return device

def test_toggle_pin(device):
    """
    Test that toggling a pin changes its state and returns back to the original state after two toggles.

    This test performs the following steps:
        1. Reads the initial state of the 'pin1' configured as an input.
        2. Calls `toggle_pin` on the device to toggle the pin state.
        3. Waits for 0.1 seconds to allow time for the toggle to happen.
        4. Reads the new state of the 'pin1' and asserts that it's different from the initial state.
        5. Calls `toggle_pin` again to toggle the pin back.
        6. Waits for 0.1 seconds to allow time for the second toggle.
        7. Reads the final state of the 'pin1' and asserts:
            - The final state is different from the state after the first toggle.
            - The final state is equal to the initial state, indicating a complete toggle cycle.

    Args:
        device (MockDAQDevice): The MockDAQDevice instance provided by the fixture.
    """
    initial_state = device.read_digital_pin('pin1')
    device.toggle_pin('pin1')
    time.sleep(0.1)  # Wait for a short time to allow toggle
    new_state = device.read_digital_pin('pin1')
    
    assert initial_state != new_state, "Pin state should have been toggled."
    
    device.toggle_pin('pin1')
    time.sleep(0.1) # Wait for a short time to allow toggle
    final_state = device.read_digital_pin('pin1')
    
    assert new_state != final_state, "Pin state should have been toggled again."
    assert initial_state == final_state, "Final state should be equal to initial state."

def test_start_blink_pin(device):
    """
    Test the start_blink_pin function to ensure it starts blinking the pin correctly.

    This test performs the following steps:
        1. Starts blinking the 'pin1' at an interval of 0.2 seconds.
        2. Waits for 0.5 seconds to allow multiple toggles.
        3. Asserts that the pin's state changes.
        4. Stops blinking the pin and ensures no more changes happen.

    Args:
        device (MockDAQDevice): The MockDAQDevice instance provided by the fixture.
    """
    device.start_blink_pin('pin1', 0.2)
    time.sleep(0.5)  # Allow some time for blinking
    first_state = device.read_digital_pin('pin1')
    time.sleep(0.3)  # Allow more time for blinking
    second_state = device.read_digital_pin('pin1')
    
    assert first_state != second_state, "Pin state should have been toggled by blinking."

    device.stop_blink_pin('pin1')
    final_state = device.read_digital_pin('pin1')
    time.sleep(0.3)  # Allow time to ensure blinking stopped
    stopped_state = device.read_digital_pin('pin1')
    
    assert final_state == stopped_state, "Pin state should not change after stopping blinking."

def test_blink_pin_error_handling(device):
    """
    Test the error handling of start_blink_pin and stop_blink_pin functions.

    This test performs the following steps:
        1. Starts blinking the 'pin1' at an interval of 0.2 seconds.
        2. Asserts that starting blinking again raises a ValueError.
        3. Stops blinking the pin.
        4. Asserts that stopping blinking again raises a ValueError.

    Args:
        device (MockDAQDevice): The MockDAQDevice instance provided by the fixture.
    """
    device.start_blink_pin('pin1', 0.2)
    
    with pytest.raises(ValueError, match="Pin is already blinking."):
        device.start_blink_pin('pin1', 0.2)
    
    device.stop_blink_pin('pin1')
    
    with pytest.raises(ValueError, match="Pin is not blinking."):
        device.stop_blink_pin('pin1')

if __name__ == '__main__':
    pytest.main()