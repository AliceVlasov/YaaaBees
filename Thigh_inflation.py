from time import sleep
from Safe_Controller import Safe_Controller

#setup
controller = Safe_Controller()

calf = controller.get_pouch("left_leg")
thigh = controller.get_pouch("left_thigh")

#inflating
controller.start_inflate(calf)
sleep(2)
controller.stop_inflate(calf)
sleep(5)
controller.start_inflate(thigh)
sleep(5)
controller.stop_inflate(thigh)

sleep(5)
#deflating
controller.start_deflate(calf)
sleep(2)
controller.stop_deflate(calf)
sleep(5)
controller.start_deflate(thigh)
sleep(4)
controller.stop_deflate(thigh)

#controller.cleanup()