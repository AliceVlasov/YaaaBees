import unittest
import Air
from Controller import Controller
from time import sleep
import math

class TestController(unittest.TestCase):
    called_safety_function = False
    controller = None

    def setUp(self):
        self.called_safety_function = False
        self.controller = Controller(self.safety_function)

    def tearDown(self):
        self.called_safety_function = False
        self.controller = None
    
    def safety_function(self):
        self.called_safety_function = True
    
    def test_can_start_pump_from_beginning(self):
        self.assertTrue(self.controller.can_start_pump())
    
    def test_calls_safety_function_when_inflate_exceeded(self):
        pouch = self.controller.get_pouch("cube")

        self.controller.inflate_pouch("cube")
        sleep(pouch.max_inflate + 1)
        self.assertTrue(self.called_safety_function)
        self.assertTrue(abs(pouch.inflate_status-pouch.max_inflate) < 0.2)
    
    def test_doesnt_call_safety_function_when_inflate_not_exceeded(self):
        pouch = self.controller.get_pouch("cylinder")

        self.controller.inflate_pouch("cylinder")
        sleep(pouch.max_inflate - 1)
        self.controller.stop_inflate()
        self.assertFalse(self.called_safety_function)
        self.assertTrue(pouch.inflate_status < pouch.max_inflate)

if __name__=="__main__":
    unittest.main()