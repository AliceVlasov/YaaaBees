from Safe_Controller import Safe_Controller
from time import sleep

inflate_time = 3

controller = Safe_Controller()
pouch = controller.get_pouch("cube")
controller.start_inflate(pouch)
sleep(inflate_time)
controller.stop_inflate(pouch)