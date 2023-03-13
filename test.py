"""
    Determine what voltage readings represent various curves of the flex sensor
"""

import busio
import digitalio
import board
import csv
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep, time
from Air import Pump

inflate = Pump(4,30)

#setup file writer
with open("tests.csv", "a", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Horizontal length in cm', 'average voltage reading'])

    # for each position that we want to measure for the flex sensor
    for m in range(1, 6):
        print ("move in position")
        inflate.
        sleep(5)
        print("taking measurements")
        readings = []
        starttime = time()
        while (time()-starttime < 5): # take measurements for 5 seconds
            readings.append(chan.voltage)
            sleep(0.1)
        
        #average measurements
        reading = sum(readings)/len(readings)
        
        # write to csv and print output
        writer.writerow([m/100,reading])
        print("measurement {0}: Voltage={1}".format(m/100, reading))
        sleep(2)