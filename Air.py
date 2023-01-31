"""
This is the API to interact with the air pump and valve(s) through a motorboard.

This includes starting and stopping an air pump, setting and changing the air pump power, and opening and closing the valve(s)

"""
from motors import Motors
from time import sleep

mc = Motors()

class Pump:
    def __init__(self, id, speed):
        self.id = id # location on the motorboard
        self.speed = speed # motor speed
        mc.stop_motor(id)
    
    def set_speed(self, new_speed):
        self.speed = new_speed

    def run(self):
        mc.move_motor(self.id, self.speed)
    
    def stop(self):
        mc.stop_motor(self.id)

    def run_for(self, seconds):
        self.run()
        sleep(seconds)
        self.stop()

class Valve:
    def __init__(self, id):
        self.id = id # location on the motorboard
        self.speed = 50 
    
    def open(self):
        mc.stop_motor(self.id)

    def open_for(self, seconds):
        self.open()
        sleep(seconds)
        self.close()

    def close(self):
        mc.start_motor(self.id, self.speed)
    
    def close_for(self, seconds):
        self.close()
        sleep(seconds)
        self.open()
    