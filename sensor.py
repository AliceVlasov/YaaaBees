import ms5803py

class MS5803():
    def read(i):
        return None

class Sensor:
    def read(self) -> float:
        return 0.00

class Pressure_Sensor(Sensor):
    def __init__(self):
        self.sensor = ms5803py.MS5803()
    
    def read(self):
        pressure, _ = self.sensor.read(pressure_osr=1024)
        return pressure