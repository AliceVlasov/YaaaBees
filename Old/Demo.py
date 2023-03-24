from Air import Pump, Silicone_valve, Pump_valve
from time import sleep

pump_deflate = Pump(5, 60)
pump_inflate = Pump(4, 100)
pump_valve = Pump_valve(2, "pump_valve")
silicone_valve = Silicone_valve(3, "silicone_valve")

# inflating
pump_valve.open_inflate()
pump_inflate.run()
sleep(10)
pump_inflate.stop()

#deflating
pump_valve.open_deflate()
pump_deflate.run()
sleep(3) 
pump_deflate.stop()

sleep(2)

pump_valve.reset()
silicone_valve.reset();

#pump.set_speed(50)

