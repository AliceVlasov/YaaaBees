from Cube_Controller import Cube_Controller
from time import sleep

inflate_time = 3

def safety_stop():
    print("STOPPPED")
    
controller = Cube_Controller(safety_stop)
controller.start_inflate(False)
sleep(2)
controller.stop_inflate(False)
#print("pressure: ",controller.cube.pressure())

#controller.stop_inflate(False)
#controller.inflate_to_size(6)
#controller.inflate_to_size(4)

#controller = Cube_Controller(safety_stop)

#print("REGULAR INFLATING")
#controller.start_inflate(False)
#sleep(inflate_time)
#controller.stop_inflate(False)

#print("RESETTING")
#controller.reset_pouch()

#print("INFLATING WITH SAFETY")
#controller.start_inflate(True)
#sleep(30)
#controller.start_deflate(True)

#print("RESETTING")
#controller.reset_pouch()

#print("INFLATING WITH SAFETY NO OVERRIDE")
#controller.start_inflate(True)
#sleep(2)
#controller.stop_inflate(True)

#print("DEFLATING WITH SAFETY NO OVERRIDE")
#controller.start_deflate(True)
#sleep(2)
#controller.stop_deflate(True)

#print("RESETTING")
#controller.reset_pouch()

