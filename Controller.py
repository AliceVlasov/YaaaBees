"""
    This file is the home of our hardware configuration including the pumps and valves we are using, the silicone
    pouches and their inflate and deflate rates, and all the functions needed for Air and GUI to communicate with each other.
"""
from typing import Callable
from time import time, sleep
from Air import Pump, Pouch, Pump_valve
from threading import Thread

_INFLATE_PUMP_PORT = 4
_DEFLATE_PUMP_PORT = 5
_PUMP_VALVE_PORT = 2

class Controller:
    def __init__(self, gui_safety_stop: Callable[[str], None]):
        """
            Initialise a new mannequin Controller

            :param gui_safety_stop: function to be called when the GUI needs to be overridden because a pouch has been inflating or deflating for too long.
        """
        self.inflate_pump = Pump(_INFLATE_PUMP_PORT, 0)
        self.deflate_pump = Pump(_DEFLATE_PUMP_PORT, 0)
        self.pump_valve = Pump_valve(_PUMP_VALVE_PORT, "pump_valve")
        self.pouches = {
            'cube':            Pouch("cube", 100,100, 3),
            'thick sleeve':    Pouch("thick_sleeve", 100, 80, 3),
            'cylinder':        Pouch("cylinder", 50, 50, 3),
            'cylinder sleeve': Pouch("cylinder_sleeve", 75, 60, 3),
            'thiccc_thigh':    Pouch("thiccc_thigh", 100, 60, 3),
            'calf':            Pouch("calf", 60, 60, 1),
        }

        # for monitoring which pouches are inflating/deflating
        self.inflating_pouch = None
        self.deflating_pouch = None
        self.start_time = None #time when pouch started inflating/deflating
        self.timer = None

        self.gui_safety_stop = gui_safety_stop # function to call to emergency override the UI
    
    def inflate_pouch(self, pouch_name:str) -> bool:
        """
            Opens valve configuration for this pouch and starts the inflate pump.

            :param pouch_name: the name of the pouch that should be inflated
            :return: whether inflating was activated successfully or not 
        """
        if str(pouch_name) not in self.pouches:
            print("Invalid pouch id:", pouch_name)
            return False
        elif self.inflating_pouch != None:
            print("Pouch {} is already inflating.".format(self.deflating_pouch.name))
            return False
        elif self.deflating_pouch != None:
            print("Must stop deflating pouch {} before inflating another.".format(self.inflating_pouch.name))
            return False
        
        self.inflating_pouch = self.pouches.get(pouch_name)

        # open correct valves
        self.pump_valve.open_inflate()
        self.inflate_pump.set_speed(self.inflating_pouch.inflate_speed)
        self.inflate_pump.run()
        self.inflating_pouch.open_valve()

        self.start_waiting_for_stop(self.inflating_pouch.get_inflate_left())

        return True
    
    def stop_inflate(self):
        self.inflating_pouch.close_valve()
        self.inflating_pouch = None
        self.inflate_pump.stop()
    
    def deflate_pouch(self, pouch_name:str) -> bool:
        """
            Opens valve configuration for this pouch and starts the deflate pump.

            :param pouch_name: the name of the pouch that should be deflated
            :return: whether deflating was activated successfully or not 
        """
        if str(pouch_name) not in self.pouches:
            print("Invalid pouch id:", pouch_name)
            return False
        elif self.deflating_pouch != None:
            print("Pouch {} is already deflating.".format(self.deflating_pouch.name))
            return False
        elif self.inflating_pouch != None:
            print("Must stop inflating pouch {} before deflating another.".format(self.inflating_pouch.name))
            return False

        self.deflating_pouch = self.pouches.get(pouch_name)

        # open correct valves
        self.pump_valve.open_deflate()
        self.deflate_pump.set_speed(self.deflating_pouch.deflate_speed)
        self.deflate_pump.run()
        self.deflating_pouch.open_valve()

        self.start_waiting_for_stop(self.deflating_pouch.get_inflate_left())

        return True
    
    def stop_deflate(self):
        self.deflating_pouch.close_valve()
        self.deflating_pouch = None
        self.deflate_pump.stop()
    
    def reset_pouch(self, pouch: Pouch):
        time_left = pouch.inflate_status
        if time_left > 0:
            self.deflate_pouch(pouch.name)
            sleep(time_left)
            self.stop_deflate()
        else:
            self.inflate_pouch(pouch.name)
            sleep(time_left)
            self.stop_inflate()
        
        pouch.inflate_status = 0
    
    def start_waiting_for_stop(self, max_time:float):
        pass #TODO

    def emergency_stop_pumps(self):
        pass
    
    def cleanup(self):
        """
            Make sure all the pouches are reset and valves are in neutral position before shutting off
        """
        
        for (_, pouch) in self.pouches:
           self.reset_pouch(pouch) 
           pouch.reset_valve()

        self.pump_valve.reset()

class Monitor:
    def __init__(self):
        """
            Initialise a new Monitor which can count the duration between events (in a separate thread)
        """
        self.time_elapsed = 0 #where to retrieve the time elapsed by the timer
        self.continue_counting = True
        self.time_elapsed = 0
    
    def countdown(self, target: float):
        start_time = time()
        while self.continue_counting and time.time()-start_time < target:
            sleep(0.1)
        
        time_elapsed = time.time()-start_time