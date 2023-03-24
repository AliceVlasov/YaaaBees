from Safe_Controller import Safe_Controller
from Cube_Controller import Cube_Controller
from time import sleep

inflate_time = 3

def safety_stop():
    print("STOPPPED")
    
controller = Cube_Controller(safety_stop)
controller.start_inflate(True)
sleep(5)
controller.stop_inflate(True)
sleep(2)
controller.start_deflate(True)
sleep(2)
controller.stop_deflate(True)

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

