from Safe_Controller import Safe_Controller
from Cube_Controller import Cube_Controller
from time import sleep

inflate_time = 3

controller = Cube_Controller()
controller.stop_inflate()
controller.stop_deflate()
controller.inflate_to_size(6)
sleep(10)
controller.inflate_to_size(5)
sleep(10)
controller.inflate_to_size(4)
sleep(10)
controller.inflate_to_size(3)
sleep(10)


controller.reset_pouch()

