"""
This is the API to interact with the air pump and valve(s) through a motorboard.

This includes starting and stopping an air pump, setting and changing the air pump power, and opening and closing the valve(s)

"""
#from motors import Motors
from time import sleep

mc = "" # Motors()

class Pump:
    def __init__(self, id, speed):
        self.id = id # location on the motorboard
        self.speed = speed # motor speed
    
    def set_speed(self, new_speed):
        self.speed = new_speed

    def run(self):
        print("starting pump {}".format(self.id))
        mc.move_motor(self.id, self.speed)

    def runWithSpeed(self, speed):
        print("starting pump {}".format(self.id))
        mc.move_motor(self.id, speed)

    def stop(self):
        print("stopping pump {}".format(self.id))
        mc.stop_motor(self.id)
        
    def run_for(self, seconds):
        self.run()
        sleep(seconds)
        self.stop()

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
        mc.stop_motor(self.id)

    def open_inflate(self):
        print("closing valve {}".format(self.name))
        mc.move_motor(self.id, self.speed)

class Silicone_valve:
    """
        This is a valve that retains air in a silicone pouch or allows air in/out.
    """
    def __init__(self, id, name):
        self.id = id # location on the motorboard
        self.speed = 100 # need this to be 100 or the valve won't close
        self.name = name
    
    def open(self):
        print("opening valve {}".format(self.name))
        mc.stop_motor(self.id)

    def close(self):
        print("closing valve {}".format(self.name))
        mc.move_motor(self.id, self.speed)
    
class Sensor:
    def __init__(self, id):
        self.id = id
        self.val = 0 # GET value from Sensor.

    def updateVal(self, val):
        self.value = val
