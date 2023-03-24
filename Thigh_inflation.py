from time import sleep
from Safe_Controller import Safe_Controller

#setup
controller = Safe_Controller()

calf = controller.get_pouch("left_leg")
thigh = controller.get_pouch("left_thigh")
cube = controller.get_pouch("cube")

#inflating

controller.start_inflate(calf)
sleep(2)
controller.stop_inflate(calf)
#sleep(5)
#controller.start_inflate(thigh)
#sleep(5)
#controller.stop_inflate(thigh)
#sleep(5)
#controller.start_inflate(cube)
#sleep(10)
#controller.stop_inflate(cube)

sleep(15)

#sleep(5)
#deflating
controller.start_deflate(calf)
sleep(1)
controller.stop_deflate(calf)
#sleep(5)
#controller.start_deflate(thigh)
#sleep(4)
#controller.stop_deflate(thigh)
#sleep(3)
#controller.start_deflate(cube)
#sleep(4)
#controller.stop_deflate(cube)

#controller.cleanup()