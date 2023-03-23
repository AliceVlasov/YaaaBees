from typing import Callable, Tuple
from threading import Timer, Thread
from time import time, sleep
from sensor import Sensor

class Monitor():
    def __init__(self, complete_callback: Callable, canceled_callback: Callable):
        self.complete_callback = complete_callback
        self.canceled_callback = canceled_callback
    
    def start(self):
        self.complete_callback()
    
    def cancel(self):
        self.canceled_callback()

def Timer(Monitor):
    def __init__(self, complete_callback: Callable, canceled_callback: Callable, max_time: float):
        super().__init__(complete_callback, canceled_callback)
        self.max_time = max_time
    
    def start(self):
        self.start_time = time()
        self.Timer = Timer(self.max_time, self.complete_callback)
        self.Timer.start()
    
    def cancel(self):
        self.Timer.cancel()
        time_elapsed = time()-self.start_time
        self.canceled_callback(time_elapsed)

def Sensor_Monitor(Monitor):
    def __init__(self, complete_callback: Callable, canceled_callback: Callable, sensor: Sensor, sensor_reading_range: Tuple[float, float]):
        super().__init__(complete_callback, canceled_callback)
        self.sensor_reading_range = self.sensor_reading_range
        self.sensor = sensor
        self.thread = Thread(target=watch_pressure)
    
    def start(self):
        self.continue_waiting = True
        self.sensor_readings_in_range = self.readings_in_range()
        self.thread.start()
    
    def readings_in_range(self) -> bool:
        reading = self.sensor.read()
        return reading >= sensor_reading_range[0] and reading <= sensor_reading_range[1]:
    
    def watch_pressure(self):
        while self.reading_in_range and self.continue_waiting:
            sleep(0.1)
            
        if self.continue_waiting:
            self.complete_callback()
    
    def cancel(self):
        self.continue_waiting = False
        self.canceled_callback()
    
