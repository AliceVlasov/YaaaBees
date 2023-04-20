from motors3 import Motors
from time import time, sleep

mc = Motors()

# IDs for pump and valve on the motorboard
pump_id = 1
valve_id = 0

# speed (power)
pump_speed = 50
valve_speed = 50

# start the motor
mc.move_motor(pump_id, pump_speed)
sleep(5)

# stop everything
mc.stop_motor(pump_id)
mc.move_motor(valve_id, valve_speed)
sleep(10)
mc.stop_motor(valve_id)
