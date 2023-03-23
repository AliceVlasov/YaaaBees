import ms5803py
from Air import Sensor

class Sensor:
    def read(self) -> float:
        return 0.00

class Pressure_Sensor(Sensor):
    def __init__(self):
        self.sensor = ms5803py.MS5803()
    
    def read(self):
        pressure, _ = self.s.read(pressure_osr=4096)
        return pressure