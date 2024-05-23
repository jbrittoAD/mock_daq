import time
import logging
import threading
from random import randint

"""
TODO list:
    * Make analog input and output
    * Make communication simulator
    * Make limits to delay tolerance before hardware test
"""

# Basic config of logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MockDAQDevice:
    def __init__(self):
        """
        Initializes the MockDAQDevice class.

        This method creates an empty dictionary `self.pins` to store pin configurations
        and sets the minimum and maximum delay values for random delays in nanoseconds.
        """
        self.pins = {}
        self.delay_min = 1  # Minimum delay to change the port state, is in nanoseconds
        self.delay_max = 1000 # Tolerance delay to change the port state, is in nanoseconds
        self.blink_threads = {}
        self.lock = threading.Lock()
        
        logger.info("MockDAQDevice initialized.")


    def change_delay_min(self, value:int):
        """
        Changes the minimum delay value used for generating random delays.

        This method updates the `self.delay_min` attribute with the provided integer value 
        (in nanoseconds) which represents the new minimum delay for the `random_microsecond_delay` function.

        Args:
            value (int): The new minimum delay value in nanoseconds.
        """
        self.delay_min = value
        
        
    def change_delay_max (self, value:int):
        """
        Changes the maximum delay value used for generating random delays.

        This method updates the `self.delay_max` attribute with the provided integer value 
        (in nanoseconds) which represents the new maximum delay for the `random_microsecond_delay` function.

        Args:
            value (int): The new maximum delay value in nanoseconds.
        """
        self.delay_max  = value

    def random_microsecond_delay(self):
        """
        Generates a random delay between the configured minimum and maximum values.

        This method generates a random integer between `self.delay_min` and `self.delay_max` (inclusive), 
        representing the delay in nanoseconds. It then uses `time.nanosleep` to wait for the specified delay.

        This function simulates the delay behavior of a physical device.
        """
        # Random delay to simulate hardware variability
        delay_nanoseconds = randint(self.delay_min, self.delay_max )
        # Sleep for the desired duration
        time.nanosleep(delay_nanoseconds)

    def configure_digital_channel(self, pin:str, direction:str):
        """
        Configures a digital pin as input or output.

        This method adds a new entry to the `self.pins` dictionary for the specified pin (`pin`). 
        The entry includes the direction (`direction`, either 'input' or 'output') and the initial state (`state`, False).

        Args:
            pin (str): The name of the digital pin to configure.
            direction (str): The direction to configure the pin ('input' or 'output').

        Raises:
            ValueError: If the provided direction is not 'input' or 'output'.
        """
        if direction not in ('input', 'output'):
            raise ValueError("Invalid direction. Must be 'input' or 'output'.")

        self.pins[pin] = {
            'direction': direction,
            'state': False,
            'blink': False
        }
        logger.debug(f"Configured pin {pin} as {direction}.")

    def write_digital_pin(self, pin:str, state:bool):
        """
        Writes a digital state (HIGH or LOW) to a configured output pin.

        This method checks if the specified pin (`pin`) exists in the `self.pins` dictionary 
        and if it's configured as an output ('output'). If both conditions are met, it updates 
        the pin's state (`state`) with the provided value.

        Args:
            pin (str): The name of the digital pin to write to.
            state (bool): The digital state to write (True for HIGH, False for LOW).

        Raises:
            ValueError: If the pin is not configured as output or does not exist.
        """
        if pin in self.pins and self.pins[pin]['direction'] == 'output':
            self.pins[pin]['state'] = state
            logger.debug(f"Pin {pin} set to {'HIGH' if state else 'LOW'}.")
        else:
            logger.error(f"Attempt to write to pin {pin} which is not configured as output or does not exist.")
            raise ValueError("Pin not configured as output or does not exist.")

    def read_digital_pin(self, pin:str):
        """
        Reads the digital state (HIGH or LOW) of a configured input pin.

        This method checks if the specified pin (`pin`) exists in the `self.pins` dictionary 
        and if it's configured as an input ('input'). If both conditions are met, it retrieves 
        the pin's state (`state`) and returns it.

        Args:
            pin (str): The name of the digital pin to read from.

        Returns:
            bool: The digital state of the pin (True for HIGH, False for LOW).

        Raises:
            ValueError: If the pin is not configured as input or does not exist.
        """
        if pin in self.pins and self.pins[pin]['direction'] == 'input':
            state = self.pins[pin]['state']
            logger.debug(f"Read pin {pin}: {'HIGH' if state else 'LOW'}.")
            return state
        else:
            logger.error(f"Attempt to read from pin {pin} which is not configured as input or does not exist.")
            raise ValueError("Pin not configured as input or does not exist.")

    def toggle_pin(self, pin):
        """
        Toggles the state of a configured input pin at a specified interval.

        This method checks if the specified pin (`pin`) exists and is configured as an input 
        ('input'). If so, it inverts the pin's state (`state`) and logs the change. Finally, 
        it logs a message indicating the start of toggling the pin at the provided interval 
        (in seconds).

        Args:
            pin (str): The name of the digital pin to toggle.
            interval (int, optional): The interval (in seconds) between toggles. Defaults to 1.

        Raises:
            ValueError: If the pin is not configured as input or does not exist.
        """
        if pin not in self.pins:
            logger.error(f"Attempt to toggle pin {pin} which does not exist.")
            raise ValueError("Pin does not exist.")
        if self.pins[pin]['direction'] != 'input':
            logger.error(f"Attempt to toggle pin {pin} which is not configured as input.")
            raise ValueError("Pin is not configured as input.")
        self.pins[pin]['state'] = not self.pins[pin]['state']
        logger.debug(f"Toggled pin {pin} to {'HIGH' if self.pins[pin]['state'] else 'LOW'}.")
    
    def _blink_pin(self, pin: str, interval: float):
        """
        Internal method to blink a pin at a specified interval.

        This method runs in a separate thread and toggles the pin state at the given interval
        until the `blink` field is set to False.

        Args:
            pin (str): The name of the digital pin to blink.
            interval (float): The interval (in seconds) between toggles.
        """
        while self.pins[pin]['blink']:
            self.toggle_pin(pin)
            time.sleep(interval)

    def start_blink_pin(self, pin: str, interval: float):
        """
        Starts blinking a pin at a specified interval.

        This method creates a new thread to toggle the pin state at the given interval. If a 
        thread is already running for the specified pin, it raises an error.

        Args:
            pin (str): The name of the digital pin to blink.
            interval (float): The interval (in seconds) between toggles.

        Raises:
            ValueError: If the pin is already blinking or does not exist.
        """
        with self.lock:
            if pin not in self.pins:
                logger.error(f"Attempt to start blinking pin {pin} which does not exist.")
                raise ValueError("Pin does not exist.")
            if self.pins[pin]['blink']:
                logger.error(f"Attempt to start blinking pin {pin} which is already blinking.")
            self.pins[pin]['blink'] = True
            blink_thread = threading.Thread(target=self._blink_pin, args=(pin, interval))
            self.blink_threads[pin] = blink_thread
            blink_thread.start()
            logger.debug(f"Started blinking pin {pin} every {interval} seconds.")

    def stop_blink_pin(self, pin: str):
        """
        Stops blinking a pin.

        This method stops the thread that is blinking the specified pin and sets the `blink` 
        field to False.

        Args:
            pin (str): The name of the digital pin to stop blinking.

        Raises:
            ValueError: If the pin is not blinking or does not exist.
        """
        with self.lock:
            if pin not in self.pins:
                logger.error(f"Attempt to stop blinking pin {pin} which does not exist.")
                raise ValueError("Pin does not exist.")
            if not self.pins[pin]['blink']:
                logger.error(f"Attempt to stop blinking pin {pin} which is not blinking.")
            self.pins[pin]['blink'] = False
            self.blink_threads[pin].join()
            del self.blink_threads[pin]
            logger.debug(f"Stopped blinking pin {pin}.")