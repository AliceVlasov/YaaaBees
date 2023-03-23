"""
    This file is the home of our hardware configuration including the pumps and valves we are using, the silicone
    pouches and their inflate and deflate rates, and all the functions needed for Air and GUI to communicate with each other.
"""
from typing import Tuple, Callable
from time import time, sleep
from Air import Pump, Pressure_Pouch, Pump_valve
from threading import Thread

_INFLATE_PUMP_PORT = 4
_DEFLATE_PUMP_PORT = 5
_PUMP_VALVE_PORT = 2

class Cube_Controller:
    def __init__(self, gui_safety_stop: Callable):
        """
            Initialise a new controller for the cube

            :param gui_safety_stop: function to call if the user causes the cube's pressure to exceed safe bounds
        """
        self.inflate_pump = Pump(_INFLATE_PUMP_PORT, 0)
        self.deflate_pump = Pump(_DEFLATE_PUMP_PORT, 0)
        self.pump_valve = Pump_valve(_PUMP_VALVE_PORT, "pump_valve")
        self.cube = Pressure_Pouch("cube", 100, 80, [3,4,5,6], [966, 969, 974, 986], 3)
        
        self.pressure_monitor = None
        self.keep_monitoring = False
        self.reset_pouch()

        self.gui_safety_stop = gui_safety_stop

        self.inflating = False
        self.deflating = False
    
    def start_pressure_monitor(self):
        """
            Starts a new thread that will wait for keep_monitoring to be set to False or for the cube's pressure to exceed the range specified at initialisation
        """
        self.keep_monitoring = True

        self.pressure_monitor = Thread(target=self.monitor_pressure)
        self.pressure_monitor.start()
        print("started pressure monitor")
    
    def stop_pressure_monitor(self):
        """
            Stops existing the thread  (if any) that is waiting for keep_monitoring to be set to False or for the cube's pressure to exceed the range specified at initialisation
        """
        self.keep_monitoring = False
        print("pressure monitor thread stopped")

        if self.pressure_monitor != None and self.pressure_monitor.is_alive():            
            self.pressure_monitor.join()
                
        self.pressure_monitor = None
    
    def start_deflate(self, with_safety_monitor: bool):
        """
            Starts deflating pouch and the pressure safety monitor if requested

            :param with_safety_monitor: whether the safety monitor, which will automatically trigger stop deflating after the safe pressure range is exceeded, should be started
        """
        self.pump_valve.open_deflate()
        self.deflate_pump.set_speed(self.cube.deflate_speed)
        self.deflate_pump.run()
        self.cube.open_valve()

        self.deflating = True

        if with_safety_monitor:
            self.start_pressure_monitor()

        print("Started deflating cube")
    
    def stop_deflate(self, with_safety_monitor: bool):
        """
            Stops the deflating pumps and closes the currently open pouch valve, and stops the safety monitor if applicable

            :param with_safty_monitor: whether a safety monitor might be running
        """
        self.cube.close_valve()
        self.deflate_pump.stop()
        self.pump_valve.reset()

        self.deflating = False

        if with_safety_monitor:
            self.stop_pressure_monitor()

        print("Stopped deflating cube")

    def start_inflate(self, with_safety_monitor: bool):
        """
            Starts inflating pouch and the pressure safety monitor if requested

            :param with_safety_monitor: whether the safety monitor, which will automatically trigger stop inflating after the safe pressure range is exceeded, should be started
        """
        self.pump_valve.open_inflate()
        self.inflate_pump.set_speed(self.cube.inflate_speed)
        self.inflate_pump.run()
        self.cube.open_valve()

        self.inflating = True

        if with_safety_monitor:
            self.start_pressure_monitor()

        print("Started inflating cube")
    
    def stop_inflate(self, with_safety_monitor: bool):
        """
            Stops the inflating pumps and closes the currently open pouch valve, and stops the safety monitor if applicable

            :param with_safty_monitor: whether a safety monitor might be running
        """
        self.cube.close_valve()
        self.inflate_pump.stop()
        self.pump_valve.reset()

        self.inflating = False

        if with_safety_monitor:
            self.stop_pressure_monitor()

        print("Stopped inflating cube")
    
    def monitor_pressure(self):
        """
            Waits until the cube is no longer in a safe pressure range or self.keep_monitoring is set to False (by the main Thread).
            Once this condition is met, it checks if loop was stopped by unsafe pressure or by the main thread. If it was the main thread,
            no further action must be taken, if it was cause by unsafe pressure readings, then emergency stop is triggered.
        """
        prev_pressure = self.cube.pressure()
        
        while self.cube_pressure_in_range() and self.keep_monitoring:
            sleep(0.1)
            
            # check that the pressure is changing at all!
            nxt_pressure = self.cube_pressure()
            if abs(next_pressure - prev_pressure()) < 1:
                print("pressure is not changing")
                self.keep_monitoring = False
            else:
                prev_pressure = next_pressure
        
        if self.keep_monitoring:
            self.emergency_stop()
    
    def emergency_stop(self):
        """
            Stops whichever pumps are running and tells the gui to reflect the changes
        """
        print("emergency stopping pumps")
        if self.inflating:
            self.stop_inflate(False)
            self.gui_safety_stop()
        elif self.deflating:
            self.stop_deflate(False)
            self.gui_safety_stop()
    
    def cube_pressure_in_range(self) -> bool:
        """
            :return: whether the cube is still within a safe pressure range
        """
        return self.cube.pressure_within_range()
        
    def reset_pouch(self):
        """
            Deflates the pouch until its base pressure is reached
        """
        base_pressure = self.cube.get_base_pressure()

        self.start_deflate(False)
        while(self.cube.pressure() > base_pressure):
            sleep(0.1)
        self.stop_deflate(False)

        self.start_inflate(False)
        while(self.cube.pressure() < base_pressure):
            sleep(0.1)
        self.stop_inflate(False)
    
    def reach_pressure(self, target_pressure:float) -> bool:
        pressure_is_changing = True
        prev_pressure = self.cube.pressure()
        
        sgn = cmp(target_pressure, prev_pressure)
        
        # figure out if we should be inflating or deflating
        if sgn < 1:
            self.start_deflate(False)
        elif sgn > 1:
            self.start_inflate(False)
        
        cur_sgn = sgn
        # continue inflating/deflating while the difference between the current pressure and target pressure is large,
        # while the current pressure does not overpass the target pressure, and the pressure continues to change
        while (abs(prev_pressure-target_pressure) > 1 and sgn == cur_sgn and pressure_is_changing):
            sleep(0.1)
            next_pressure = self.cube.pressure()
            cur_sgn = 
            
            if abs(next_pressure - prev_pressure()) < 1:
                print("pressure not changing")
                pressure_is_changing = False
                
        
        
        # stop inflating
        self.stop_inflate(False)
        
        if not pressure_is_change:
            return False

        return True
        
    
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

        return self.reach_pressure(inflate_pressure)
    
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
        

    
    