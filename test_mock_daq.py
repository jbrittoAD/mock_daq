import unittest
import time
from mock_daq import MockDAQDevice

class TestMockDAQDevice(unittest.TestCase):

    def setUp(self):
        self.device = MockDAQDevice()
        self.device.configure_digital_channel('pin1', 'input')

    def test_toggle_pin(self):
        self.device.toggle_pin('pin1', interval=1)
        
        initial_state = self.device.read_digital_pin('pin1')
        time.sleep(1.1)  # Espera um pouco mais de um segundo
        new_state = self.device.read_digital_pin('pin1')
        
        self.assertNotEqual(initial_state, new_state, "O estado do pino deveria ter sido alternado.")
        
        time.sleep(1.1)
        final_state = self.device.read_digital_pin('pin1')
        
        self.assertNotEqual(new_state, final_state, "O estado do pino deveria ter sido alternado novamente.")
        self.assertEqual(initial_state, final_state, "O estado final deveria ser igual ao estado inicial.")

if __name__ == '__main__':
    unittest.main()
