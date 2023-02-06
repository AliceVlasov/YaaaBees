from Air import Pump, Valve
from time import sleep

# initialise the pumps and valves
pump_1 = Pump(1, 50)
valve_1 = Valve(0, 50)

pump_1.run()
sleep(5)
valve_1.open()
sleep(5)
valve_1.close()
sleep(5)
pump_1.stop()