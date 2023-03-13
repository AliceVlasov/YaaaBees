from time import sleep
from Controller import Controller

#setup
controller = Controller()

#inflating
controller.inflate_pouch("cube")
sleep(3)
controller.stop_inflate()

#deflating
controller.deflate_pouch("cube")
sleep(3)
controller.stop_deflate()

#cleanup
controller.cleanup()