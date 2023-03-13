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

#create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

#create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

#create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog nput channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

#setup file writer
with open("flex_test_vertical_measurements.csv", "a", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Horizontal length in cm', 'average voltage reading'])

    # for each position that we want to measure for the flex sensor
    for m in range(0,501,25):
        print ("move in position")
        sleep(3)
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
