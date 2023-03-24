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
    def __init__(self, gui_safety_stop):
        """
            Initialise a new controller for the cube

            :param gui_safety_stop: function to call if the user causes the cube's pressure to exceed safe bounds
        """
        self.inflate_pump = Pump(_INFLATE_PUMP_PORT, 0)
        self.deflate_pump = Pump(_DEFLATE_PUMP_PORT, 0)
        self.pump_valve = Pump_valve(_PUMP_VALVE_PORT, "pump_valve")
        self.cube = Pressure_Pouch("cube", 100, 80, [3,4,5,6], [966, 969, 974, 986], 0)
        
        self.pressure_monitor = None
        self.keep_monitoring = False
        self.reset_pouch()

        self.gui_safety_stop = gui_safety_stop

        self.inflating = False
        self.deflating = False
        
        #self.reset_pouch()
        print("FINISHED SETUP")
    
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
        print("pressure monitor started")
        starting_pressure = self.cube.pressure()
        pressure_changing = True
        
        if not self.cube.sensor.is_working():
            sensor_working = False
        
        counter = 0
        
        while self.safe_pressure() and self.keep_monitoring and sensor_working and pressure_changing:
            sleep(0.1)
            
            # check that the pressure is changing at all!
            cur_pressure = self.cube.pressure() if self.cube.sensor.is_working() else starting_pressure
            counter += 1
            
            if counter == 10:
                counter = 0      
                if abs(cur_pressure - starting_pressure) < 0.5:
                    print("pressure is not changing")
                    pressure_changing = False
            
            self.sensor_working = self.cube.sensor.is_working()
        
        if self.keep_monitoring:
            print("Pressure exceeded safe range")
            self.emergency_stop()
        
        if not sensor_working:
            print("stopping monitor because sensor is not working")
            self.emergency_stop()
        
        if not pressure_changing:
            print("stopping monitor because pressure is not changing")
            self.emergency_stop()
            
    
    def safe_pressure(self) -> bool:
        in_range = self.cube_pressure_in_range()
        
        if in_range == -2:
            return False
        if in_range == 0:
            return True
        if in_range < 0 and self.inflating:
            return True
        if in_range > 0 and self.deflating:
            return True
        
        return False
        
    
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
    
    def cube_pressure_in_range(self) -> int:
        """
            :return: -1 if pressure below safe range, 0 if pressure within safe range, 1 if pressure above safe range
        """
        return self.cube.pressure_within_range()
        
    def reset_pouch(self) -> bool:
        """
            Deflates the pouch until its base pressure is reached

            :return: whether the pouch was reset successfully or not
        """
        base_pressure = self.cube.get_base_pressure()
        
        if not self.cube.sensor.is_working():
            return False

        return self.reach_pressure(base_pressure)
    
    def cmp(self, a: float, b: float) -> int:
        if a < b:
            return -1
        if a > b:
            return 1
        return 0
    
    def reach_pressure(self, target_pressure:float) -> bool:
        pressure_is_changing = True
        start_pressure = self.cube.pressure()
        prev_pressure = start_pressure
        
        if not self.cube.sensor.is_working():
            return False
        
        sgn = self.cmp(target_pressure, prev_pressure)
        print("target pressure = {0}, start_pressure = {1}".format(target_pressure, start_pressure))
        
        # figure out if we should be inflating or deflating
        if sgn < 0:
            self.start_deflate(False)
        elif sgn > 0:
            self.start_inflate(False)
        
        cur_sgn = sgn
        print("sgn = {0}".format(sgn))
        
        counter = 0
        # continue inflating/deflating while the difference between the current pressure and target pressure is large,
        # while the current pressure does not overpass the target pressure, and the pressure continues to change
        while (abs(prev_pressure-target_pressure) > 1 and sgn == cur_sgn and pressure_is_changing):
            sleep(0.1)
            next_pressure = self.cube.pressure() if self.cube.sensor.is_working() else prev_pressure
            counter += 1
            
            if counter == 10:          
                if abs(next_pressure - start_pressure) < 0.5:
                    print("pressure not changing")
                    pressure_is_changing = False
                counter = 0
            
            cur_sgn = self.cmp(target_pressure, next_pressure)

            prev_pressure = next_pressure
        
        print("exited")
        
        if (sgn != cur_sgn):
            print("sgn != cur_sgn")

        print("target pressure {0}, stopped at pressure {1}".format(target_pressure, self.cube.pressure()))
        
        # stop inflating or deflating
        if sgn < 0:
            self.stop_deflate(False)
        elif sgn > 0:
            self.stop_inflate(False)
        
        if not pressure_is_changing:
            print("stopping pumps because pressure is not changing")
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
        
        print("starting inflating to size")

        return self.reach_pressure(inflate_pressure)
    
    def get_pouch_size_range(self) -> Tuple[int,int]:
        """
            :param pouch_name: the name of the pouch whose size range is desired
            :return: the minimum and maximum sizes(cm) the given pouch can achieve
        """
        sizes = self.cube.get_size_range()

        # if not pouch:
        #     print("Invalid pouch name.")
        #     return (-1,-1)
        
        return sizes
        
    def cleanup(self):
        """
            Make sure all the pouches and pumps are reset and valves are in 
            neutral position before shutting off
        """
        print("Cleaning up")
        self.stop_inflate(True)
        self.stop_deflate(True)

        self.reset_pouch()

        self.pump_valve.reset()
    