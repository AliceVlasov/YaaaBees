from Air import Pump, Valve

# initialise the pumps and valves
pump_1 = Pump(1, 50)
valve_1 = Valve(0, 50)

valve_1.open_for(15)
pump_1.run_for(5)