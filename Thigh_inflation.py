from time import sleep
from Controller import Controller

#setup
controller = Controller()

#inflating
controller.inflate_pouch("thiccc thigh")
sleep(12)
controller.stop_inflate()

controller.cleanup()