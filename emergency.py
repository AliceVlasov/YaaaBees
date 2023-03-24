from Air import Silicone_valve, Pump, Pump_valve

valve_1 = Silicone_valve(0, "0")
valve_2 = Silicone_valve(1, "1")
valve_3 = Silicone_valve(2, "2")
valve_4 = Silicone_valve(3, "3")

pump_1 = Pump(4,0)
pump_2 = Pump(5,0)

valve_1.reset()
valve_2.reset()
valve_3.reset()
valve_4.reset()

pump_1.stop()
pump_2.stop()