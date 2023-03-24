"""
This is the API to interact with the air pump and valve(s) through a motorboard.

This includes starting and stopping an air pump, setting and changing the air pump power, and opening and closing the valve(s)

"""
from motors3 import Motors
from time import sleep
from typing import List, Tuple
from sensor import Pressure_Sensor

_TESTING = False

if not _TESTING:
    mc = Motors()

class Pump:
    def __init__(self, id, speed):
        self.id = id # location on the motorboard
        self.speed = speed # motor speed
    
    def set_speed(self, new_speed):
        self.speed = new_speed

    def run(self):
        #print("starting pump {}".format(self.id))
        if not _TESTING:
            mc.move_motor(self.id, self.speed)

    def runWithSpeed(self, speed):
        #print("starting pump {}".format(self.id))
        if not _TESTING:
            mc.move_motor(self.id, speed)

    def stop(self):
        #print("stopping pump {}".format(self.id))
        if not _TESTING:
            mc.stop_motor(self.id)
        
    def run_for(self, seconds):
        self.run()
        sleep(seconds)
        self.stop()

class Pouch:
    def __init__(self, name: str, inflate_speed: int, deflate_speed: int, sizes: List[int], times: List[Tuple[float, float]], valve_id: int):
        """
            Initialise a new Silicone Pouch

            :param name: a unique name to identify the pouch
            :param inflate_speed: pump speed for inflating
            :param deflate_speed: pump speed for deflating
            :param sizes: list of sizes (cm) that the pouch can achieve 
            :param times: list of times (s) needed for the pouch to inflate to each size in sizes 
            :param valve_id: the port motorboard port number for the valve controlling air inside the pouch
        """
        self.name = name
        self.inflate_speed = inflate_speed
        self.deflate_speed = deflate_speed

        self.valve = Silicone_valve(valve_id, name+" valve")

        # make dictionary of size to inflate/deflate times
        self.sizes = dict()
        for (s,t) in list(zip(sizes, times)):
            self.sizes[s] = [t[0], t[1]]

        sorted_sizes = sorted(sizes)
        self.size_range = (sorted_sizes[0], sorted_sizes[-1])

        self.current_size = sizes[0] # pouch starts neutral

        # make sure valve is closed by default
        self.close_valve()
    
    def get_deflate_needed(self) -> float:
        """
            :return: the amount of time needed to deflate this pouch until it reaches its neutral state
        """
        return self.sizes[self.current_size][1]
    
    def get_inflate_time_for_size(self, size: int):
        """
            Returns the number of seconds needed for the pouch to inflate to the given size. If that size is not specified for this pouch, -1 is returned
        
            :param size: the size (cm) setting for this pouch
        """
        if size not in self.sizes:
            return -1

        return self.sizes[size][0]
        
    
    def update_inflate_status(self, size: int) -> None:
        """
            Updates the net amount of time the pouch has spend inflating

            :param size: the current size of the pouch
        """
        print("pouch {0}'s size is now {1}".format(self.name, size))
        self.current_size = size
    
    def reset_inflate_status(self):
        self.current_size = self.size_range[0]
        print("reset pouch {0}'s size to {1}".format(self.name, self.current_size))
    
    def get_size_range(self) -> Tuple[int,int]:
        """
            :return: tuple with the maximum and minimum sizes (cm) that the pouch can achieve
        """
        return self.size_range
    
    def open_valve(self):
        self.valve.open()
    
    def close_valve(self):
        self.valve.close()
    
    def reset_valve(self):
        self.valve.reset()

class Pressure_Pouch(Pouch):
    def __init__(self, name: str, inflate_speed: int, deflate_speed: int, sizes: List[int], pressures: List[float], valve_id: int):
        """
            Initialise a new Silicone Pouch

            :param name: a unique name to identify the pouch
            :param inflate_speed: pump speed for inflating
            :param deflate_speed: pump speed for deflating
            :param sizes: list of sizes (cm) that the pouch can achieve starting with the neutral size
            :param pressures: list of pressures (mBar) needed for the pouch to inflate to each size in sizes 
            :param valve_id: the port motorboard port number for the valve controlling air inside the pouch
        """
        self.name = name
        self.inflate_speed = inflate_speed
        self.deflate_speed = deflate_speed

        self.valve = Silicone_valve(valve_id, name+" valve")

        sorted_sizes = sorted(sizes)
        self.size_range = (sorted_sizes[0], sorted_sizes[-1])

        self.inflate_status = 0 # pouch starts neutral

        # make sure valve is closed by default
        self.close_valve()

        self.pressure_sizes = dict()
        for (s,p) in list(zip(sizes, pressures)):
            self.pressure_sizes[str(s)] = p 
        
        sorted_pressures = sorted(pressures)

        self.pressure_range = (sorted_pressures[0], sorted_pressures[-1])
        self.sensor = Pressure_Sensor()
    
    def get_base_pressure(self) -> float:
        """
            :return: the pressure (mBar) of the cube when it is in its resting position
        """
        return self.pressure_range[0]

    def get_pressure_for_size(self, size: int) -> float:
        """
            :param size: the target size(cm) for this pressure pouch
            :return the target pressure for the cube to achieve the given size, or -1 if the size is not defined for the cube
        """
        if str(size) not in self.pressure_sizes:
            return -1
        
        return self.pressure_sizes[str(size)]
    
    def pressure(self) -> float:
        """
            :return: the current pressure within the cube
        """
        return self.sensor.read()

    def pressure_within_range(self) -> bool:
        """
            :return: whether the current internal pressure of the pouch is within the safe range defined at initialisation
        """
        pressure = self.pressure()
        print("current pressure = {}".format(pressure))
        print("pressure range: ({0}, {1})".format(self.pressure_range[0], self.pressure_range[1]))
        return pressure > self.pressure_range[0] and pressure < self.pressure_range[1]


class Pump_valve:
    """
        This is a valve that controls whether the output is inflating/deflating
        by connecting the pumps.
    """
    def __init__(self, id, name):
        self.id = id # location on the motorboard
        self.speed = 100 # need this to be 100 or the valve won't close
        self.name = name
    
    def open_deflate(self):
        #print("opening valve {}".format(self.name))
        if not _TESTING:
            mc.stop_motor(self.id)

    def open_inflate(self):
        #print("closing valve {}".format(self.name))
        if not _TESTING:
            mc.move_motor(self.id, self.speed)
    
    def reset(self):
        self.open_deflate()

class Silicone_valve:
    """
        This is a valve that retains air in a silicone pouch or allows air in/out.
    """
    def __init__(self, id, name):
        self.id = id # location on the motorboard
        self.speed = 100 # need this to be 100 or the valve won't close
        self.name = name
    
    def close(self):
        #print("closing valve {}".format(self.name))
        if not _TESTING:
            mc.stop_motor(self.id)

    def open(self):
        #print("opening valve {}".format(self.name))
        if not _TESTING:
            mc.move_motor(self.id, self.speed)
    
    def reset(self):
        self.close()