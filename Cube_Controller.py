"""
    This file is the home of our hardware configuration including the pumps and valves we are using, the silicone
    pouches and their inflate and deflate rates, and all the functions needed for Air and GUI to communicate with each other.
"""
from typing import Tuple
from time import time, sleep
from Air import Pump, Pouch, Pressure_Pouch, Pump_valve
from threading import Timer

_INFLATE_PUMP_PORT = 4
_DEFLATE_PUMP_PORT = 5
_PUMP_VALVE_PORT = 2

class Cube_Controller:
    def __init__(self):
        """
            Initialise a new controller for the cube
        """
        self.inflate_pump = Pump(_INFLATE_PUMP_PORT, 0)
        self.deflate_pump = Pump(_DEFLATE_PUMP_PORT, 0)
        self.pump_valve = Pump_valve(_PUMP_VALVE_PORT, "pump_valve")
        self.cube = Pressure_Pouch("cube", 100, 80, [3,4,5,6], [966, 969, 974, 986], 3)
        
        self.reset_pouch()
    
    def start_deflate(self):
        self.pump_valve.open_deflate()
        self.deflate_pump.set_speed(self.cube.deflate_speed)
        self.deflate_pump.run()
        self.cube.open_valve()

        print("Started deflating cube")
    
    def stop_deflate(self):
        self.cube.close_valve()
        self.deflate_pump.stop()
        self.pump_valve.reset()

        print("Stopped deflating cube")

    def start_inflate(self):
        self.pump_valve.open_inflate()
        self.inflate_pump.set_speed(self.cube.inflate_speed)
        self.inflate_pump.run()
        self.cube.open_valve()

        print("Started inflating cube")
    
    def stop_inflate(self):
        self.cube.close_valve()
        self.inflate_pump.stop()
        self.pump_valve.reset()

        print("Stopped inflating cube")
        
    def reset_pouch(self):
        """
            Deflates the pouch until its base pressure is reached
        """
        base_pressure = self.cube.get_base_pressure()

        self.start_deflate()
        while(self.cube.pressure() > base_pressure):
            sleep(0.1)
        self.stop_deflate()

        self.start_inflate()
        while(self.cube.pressure() < base_pressure):
            sleep(0.1)
        self.stop_inflate()
        
    
    def inflate_to_size(self, size:int) -> bool:
        """
            Inflates pouch with the given name to a specific size

            :param size: the size (cm) to which to inflate the pouch
            :return: whether the pouch was inflated successfully or not
        """

        self.reset_pouch()

        inflate_pressure = self.cube.get_pressure_for_size(size)

        if inflate_pressure == -1:
            print("Invalid size {0} for cube".format(size))
            return False

        self.start_inflate()
        while (self.cube.pressure() < inflate_pressure):
            sleep(0.1)
        self.stop_inflate()

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
        

    
    