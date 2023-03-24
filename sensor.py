import ms5803py

class MS5803():
    def read(i):
        return None

class Sensor:
    def read(self) -> float:
        return 0.00

class Pressure_Sensor(Sensor):
    def __init__(self):
        self.working = True
        try:
            self.sensor = ms5803py.MS5803()
        except Exception:
            self.sensor = None
            self.working = False
    
    def is_working(self):
        try:
            pressure, _ = self.sensor.read(pressure_osr=1024)
            self.working = True
            return True
        except Exception:
            print("cannot read sensor")
            self.working = False
            return False
    
    def read(self):
        pressure = None
        count = 0
        while (pressure == None and count < 10):
            try:
                pressure, _ = self.sensor.read(pressure_osr=1024)
                self.working = True
                return pressure
            except Exception:
                print("cannot read sensor")
                count += 1
        self.working = False
        print("sensor not working")
        return None