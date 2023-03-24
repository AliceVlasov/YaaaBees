"""
    This file is the home of our hardware configuration including the pumps and valves we are using, the silicone
    pouches and their inflate and deflate rates, and all the functions needed for Air and GUI to communicate with each other.
"""
from typing import Tuple
from time import time, sleep
from Air import Pump, Pouch, Pump_valve
from threading import Timer

_INFLATE_PUMP_PORT = 4
_DEFLATE_PUMP_PORT = 5
_PUMP_VALVE_PORT = 2

class Safe_Controller:
    def __init__(self):
        """
            Initialise a new mannequin Controller
        """
        self.inflate_pump = Pump(_INFLATE_PUMP_PORT, 0)
        self.deflate_pump = Pump(_DEFLATE_PUMP_PORT, 0)
        self.pump_valve = Pump_valve(_PUMP_VALVE_PORT, "pump_valve")
        self.pouches = {
            'cube':              Pouch("cube", 100, 80, [1,2,3], [5,7,9], 0),
            # 'thick sleeve':      Pouch("thick_sleeve", 100, 80, 4, 3),
            # 'cylinder':          Pouch("cylinder", 50, 50, 2, 3),
            # 'cylinder sleeve':   Pouch("cylinder_sleeve", 75, 60, 7, 3),
            'left_thigh':        Pouch("left_thigh", 100, 60, [1,2,3], [5,7,9], 1),
            'left_leg':          Pouch("left_leg", 100, 60, [1,2,3], [5,7,9], 3),
        }
    
    def get_pouch(self, pouch_name: str) -> Pouch:
        if pouch_name in self.pouches:
            return self.pouches[pouch_name]
    
    def start_deflate(self, pouch: Pouch):
        self.pump_valve.open_deflate()
        self.deflate_pump.set_speed(pouch.deflate_speed)
        self.deflate_pump.run()
        pouch.open_valve()

        #print("Started deflating {}".format(pouch.name))
    
    def stop_deflate(self, pouch: Pouch):
        pouch.close_valve()
        self.deflate_pump.stop()
        self.pump_valve.reset()

        #print("Stopped deflating {}".format(pouch.name))

    def start_inflate(self, pouch: Pouch):
        self.pump_valve.open_inflate()
        self.inflate_pump.set_speed(pouch.inflate_speed)
        self.inflate_pump.run()
        pouch.open_valve()

        #print("Started inflating {}".format(pouch.name))
    
    def stop_inflate(self, pouch: Pouch):
        pouch.close_valve()
        self.inflate_pump.stop()
        self.pump_valve.reset()

        #print("Stopped inflating {}".format(pouch.name))
        
    def reset_pouch(self, pouch_name: str):
        pouch = self.get_pouch(pouch_name)

        if not pouch:
            print("invalid pouch name")
            return

        print("Resetting pouch {}".format(pouch.name))

        deflate_time = pouch.get_deflate_needed() # from .get_deflate_left()

        self.start_deflate(pouch)
        sleep(deflate_time)
        self.stop_deflate(pouch)

        pouch.reset_inflate_status()
    
    def inflate_pouch_to_size(self, pouch_name:str, size:int) -> bool:
        """
            Inflates pouch with the given name to a specific size

            :param pouch_name: the name of the pouch to inflate
            :param size: the size (cm) to which to inflate the pouch
            :return: whether the pouch was inflated successfully or not
        """
        pouch = self.get_pouch(pouch_name)

        if not pouch:
            print("Invalid pouch name:", pouch_name)
            return False 

        self.reset_pouch(pouch_name)

        inflate_time = pouch.get_inflate_time_for_size(size)

        if inflate_time == -1:
            print("Invalid size {0} for pouch {1}".format(size, pouch_name))
            return False

        self.start_inflate(pouch)
        sleep(inflate_time)
        self.stop_inflate(pouch)
        pouch.update_inflate_status(inflate_time)

        return True
    
    def get_pouch_size_range(self, pouch_name: str) -> Tuple[int,int]:
        """
            :param pouch_name: the name of the pouch whose size range is desired
            :return: the minimum and maximum sizes(cm) the given pouch can achieve
        """
        pouch = self.get_pouch(pouch_name)

        if not pouch:
            print("Invalid pouch name.")
            return (-1,-1)
        
        return pouch.get_size_range()
        

    def cleanup(self):
        """
            Make sure all the pouches and pumps are reset and valves are in 
            neutral position before shutting off
        """
        print("Cleaning up")

        for pouch_name in self.pouches:
           pouch = self.get_pouch(pouch_name)
           self.reset_pouch(pouch_name) 
           pouch.reset_valve()

        self.pump_valve.reset()
    