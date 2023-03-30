from time import sleep
from Controller import Controller

#setup
controller = Controller()

#inflating
controller.inflate_pouch("thiccc thigh")
sleep(7)
controller.stop_inflate()

#deflating
controller.deflate_pouch("thiccc thigh")
sleep(5)
controller.stop_deflate()

#cleanup
controller.cleanup()