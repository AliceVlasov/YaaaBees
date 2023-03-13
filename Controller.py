"""
    This file is the home of our hardware configuration including the pumps and valves we are using, the silicone
    pouches and their inflate and deflate rates, and all the functions needed for Air and GUI to communicate with each other.
"""
from Air import Pump, Silicone_valve, Pump_valve

_INFLATE_PUMP_PORT = 4
_DEFLATE_PUMP_PORT = 5
_PUMP_VALVE_PORT = 2

class Pouch:
    def __init__(self, name: str, id: int, inflate_speed: int, deflate_speed: int, valve_id: int):
        self.name = name
        self.id = id
        self.inflate_speed = inflate_speed
        self.deflate_speed = deflate_speed
        self.valve = Silicone_valve(valve_id)

        # make sure valve is closed by default
        self.close_valve()
    
    def open_valve(self):
        self.valve.open()
    
    def close_valve(self):
        self.valve.close()

class Controller:
    def __init__(self):
        self.inflate_pump = Pump(_INFLATE_PUMP_PORT, 0)
        self.deflate_pump = Pump(_DEFLATE_PUMP_PORT, 0)
        self.pump_valve = Pump_valve(_PUMP_VALVE_PORT, "pump_valve")
        self.pouches = {
            'cube': Pouch("cube", 1, 80, 80, 3),
            'thick_sleeve': Pouch("thick_sleeve", 2, 100, 80, 3)
        }
    
    def inflate_pouch(self, pouch_name:str):
        if str(pouch_name) not in self.pouches:
            print("Invalid pouch id:", pouch_name)
            return
        
        self.inflating_pouch = self.pouches.get(pouch_name)

        # open correct valves
        self.pump_valve.open_inflate()
        self.inflate_pump.set_speed(self.inflating_pouch.inflate_speed)
        self.inflate_pump.run()
        self.inflating_pouch.open_valve()
    
    def stop_inflate(self):
        self.inflating_pouch.close_valve()
        self.inflating_pouch = None
        self.inflate_pump.stop()
    
    def deflate_pouch(self, pouch_name:str):
        if str(pouch_name) not in self.pouches:
            print("Invalid pouch id:", pouch_name)
            return
        
        self.deflating_pouch = self.pouches.get(pouch_name)

        # open correct valves
        self.pump_valve.open_inflate()
        self.deflate_pump.set_speed(self.inflating_pouch.inflate_speed)
        self.deflate_pump.run()
        self.deflating_pouch.open_valve()
    
    def stop_deflate(self):
        self.deflating_pouch.close_valve()
        self.deflating_pouch = None
        self.deflate_pump.stop()