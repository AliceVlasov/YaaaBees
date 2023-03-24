from time import sleep
from Safe_Controller import Safe_Controller

#setup
controller = Safe_Controller()

calf = controller.get_pouch("left_leg")
thigh = controller.get_pouch("left_thigh")
cube = controller.get_pouch("cube")

controller.inflate_pouch_to_size("left_leg", 19)
sleep(3)

controller.inflate_pouch_to_size("left_thigh", 26)
sleep(3)

controller.reset_pouch("left_leg")

sleep(3)

controller.reset_pouch("left_thigh")

#inflating

#controller.start_inflate(thigh)
#sleep(7)
#controller.stop_inflate(thigh)
#sleep(5)
#controller.start_inflate(thigh)
#sleep(5)
#controller.stop_inflate(thigh)
#sleep(5)
#controller.start_inflate(cube)
#sleep(10)
#controller.stop_inflate(cube)

#sleep(15)

#sleep(5)
#deflating
#controller.start_deflate(thigh)
#sleep(5)
#controller.stop_deflate(thigh)
#sleep(5)
#controller.start_deflate(thigh)
#sleep(4)
#controller.stop_deflate(thigh)
#sleep(3)
#controller.start_deflate(cube)
#sleep(4)
#controller.stop_deflate(cube)

#controller.cleanup()