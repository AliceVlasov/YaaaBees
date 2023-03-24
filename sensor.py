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
        self.is_working = True
    
    def read(self):
        pressure = None
        count = 0
        while (pressure == None and count < 10):
            try:
                pressure, _ = self.sensor.read(pressure_osr=1024)
                return pressure
            except:
                print("cannot read sensor")
                count += 1
        self.is_working = False
        print("sensor not working")
        return None