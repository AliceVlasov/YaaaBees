from time import sleep
from Controller import Controller

#setup
controller = Controller()

#inflating
controller.inflate_pouch("thiccc thigh")
sleep(6)
controller.stop_inflate()

#deflating
controller.deflate_pouch("thiccc thigh")
sleep(2)
controller.stop_deflate()

#cleanup
controller.cleanup()