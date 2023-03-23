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
        print("starting pump {}".format(self.id))
        if not _TESTING:
            mc.move_motor(self.id, self.speed)

    def runWithSpeed(self, speed):
        print("starting pump {}".format(self.id))
        if not _TESTING:
            mc.move_motor(self.id, speed)

    def stop(self):
        print("stopping pump {}".format(self.id))
        if not _TESTING:
            mc.stop_motor(self.id)
        
    def run_for(self, seconds):
        self.run()
        sleep(seconds)
        self.stop()

class Pouch:
    def __init__(self, name: str, inflate_speed: int, deflate_speed: int, sizes: List[int], times: List[float], valve_id: int):
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

        self.sizes = dict()
        for (s,t) in list(zip(sizes, times)):
            self.sizes[str(s)] = t

        sorted_sizes = sorted(sizes)
        self.size_range = (sorted_sizes[0], sorted_sizes[-1])

        self.inflate_status = 0 # pouch starts neutral

        # make sure valve is closed by default
        self.close_valve()
    
    def get_deflate_needed(self):
        return self.inflate_status
    
    def get_inflate_time_for_size(self, size: int):
        """
            Returns the number of seconds needed for the pouch to inflate to the given size. If that size is not specified for this pouch, -1 is returned
        
            :param size: the size (cm) setting for this pouch
        """
        if str(size) not in self.sizes:
            return -1

        return self.size[str(size)]
        
    
    def update_inflate_status(self, time_inflated: float) -> None:
        """
            Updates the net amount of time the pouch has spend inflating

            :param time_inflated: the amount of time this pouch has been inflating so far, if deflating, this should be negative
        """
        print("increased pouch {0}'s inflate status by {1}".format(self.name, time_inflated))
        self.inflate_status += time_inflated
    
    def reset_inflate_status(self):
        print("reset pouch {}'s inflate status to 0".format(self.name))
        self.inflate_status = 0
    
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
        super.__init__(name, inflate_speed, deflate_speed, sizes, [0 for _ in range(len(sizes))], valve_id)

        self.pressure_sizes = dict()
        for (s,p) in list(zip(sizes, pressures)):
            self.pressure_sizes[str(s)] = p 
        
        self.base_pressure = pressures[0]
        self.sensor = Pressure_Sensor()
    
    def get_base_pressure(self) -> float:
        """
            :return: the pressure (mBar) of the cube when it is in its resting position
        """
        return self.base_pressure

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
        print("opening valve {}".format(self.name))
        if not _TESTING:
            mc.stop_motor(self.id)

    def open_inflate(self):
        print("closing valve {}".format(self.name))
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
        print("closing valve {}".format(self.name))
        if not _TESTING:
            mc.stop_motor(self.id)

    def open(self):
        print("opening valve {}".format(self.name))
        if not _TESTING:
            mc.move_motor(self.id, self.speed)
    
    def reset(self):
        self.close()