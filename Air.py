"""
This is the API to interact with the air pump and valve(s) through a motorboard.

This includes starting and stopping an air pump, setting and changing the air pump power, and opening and closing the valve(s)

"""
from motors3 import Motors
from time import sleep

_TESTING = True

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
    def __init__(self, name: str, inflate_speed: int, deflate_speed: int, max_inflate: float, valve_id: int):
        """
            Initialise a new Silicone Pouch

            :param name: a unique name to identify the pouch
            :param inflate_speed: pump speed for inflating
            :param deflate_speed: pump speed for deflating
            :param max_inflate: max number of seconds that the pouch can inflate safely for
            :param valve_id: the port motorboard port number for the valve controlling air inside the pouch
        """
        self.name = name
        self.inflate_speed = inflate_speed
        self.deflate_speed = deflate_speed

        self.valve = Silicone_valve(valve_id, name+" valve")

        self.max_inflate = max_inflate   
        self.inflate_status = 0 # pouch starts neutral

        # make sure valve is closed by default
        self.close_valve()
    
    def get_inflate_left(self):
        return self.max_inflate-self.inflate_status
    
    def get_deflate_left(self):
        return self.inflate_status
    
    def update_inflate_status(self, time_inflated: float) -> None:
        """
            Updates the net amount of time the pouch has spend inflating

            :param time_inflated: the amount of time this pouch has been inflating so far, if deflating, this should be negative
        """
        self.inflate_status += time_inflated
    
    def open_valve(self):
        self.valve.open()
    
    def close_valve(self):
        self.valve.close()
    
    def reset_valve(self):
        self.valve.reset()

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
    
class Sensor:
    def __init__(self, id):
        self.id = id
        self.val = 0 # GET value from Sensor.

    def updateVal(self, val):
        self.value = val
