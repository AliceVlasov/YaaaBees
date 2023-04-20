"""
This is the API to interact with the air pump and valve(s) through a motorboard.

This includes starting and stopping an air pump, setting and changing the air pump power, and opening and closing the valve(s)

"""
from motors3 import Motors
from time import sleep

mc = Motors()

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

class Valve:
    def __init__(self, id):
        self.id = id # location on the motorboard
        self.speed = 100 # need this to be 100 or the valve won't close
        self.close()
    
    def open(self):
        print("opening valve {}".format(self.id))
        mc.stop_motor(self.id)

    def open_for(self, seconds):
        self.open()
        sleep(seconds)
        self.close()

    def close(self):
        print("closing valve {}".format(self.id))
        mc.move_motor(self.id, self.speed)
    
    def close_for(self, seconds):
        self.close()
        sleep(seconds)
        self.open()
    