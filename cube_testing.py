from Safe_Controller import Safe_Controller
from Cube_Controller import Cube_Controller
from time import sleep

inflate_time = 3

def safety_stop():
    print("STOPPPED")

controller = Cube_Controller(safety_stop)

controller.stop_inflate(False)
controller.stop_deflate(False)


#controller.start_inflate(False)
#sleep(inflate_time)
#controller.stop_inflate(False)

#controller.reset_pouch()

#controller.start_inflate(True)
#sleep(100)
#controller.start_deflate(True)

#controller.reset_pouch()

#controller.start_inflate(True)
#sleep(2)
#controller.stop_inflate(True)

#controller.start_deflate(True)
#sleep(2)
#controller.stop_deflate(True)

#controller.reset()

