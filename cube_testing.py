from Safe_Controller import Safe_Controller
from Cube_Controller import Cube_Controller
from time import sleep

inflate_time = 3

controller = Cube_Controller()
controller.stop_inflate()
sleep(inflate_time)
controller.stop_deflate()



controller.reset_pouch()

