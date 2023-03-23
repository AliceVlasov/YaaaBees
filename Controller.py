"""
    This file is the home of our hardware configuration including the pumps and valves we are using, the silicone
    pouches and their inflate and deflate rates, and all the functions needed for Air and GUI to communicate with each other.
"""
from typing import Callable
from time import time, sleep
from Air import Pump, Pouch, Pump_valve
from threading import Timer

_INFLATE_PUMP_PORT = 4
_DEFLATE_PUMP_PORT = 5
_PUMP_VALVE_PORT = 2

class Controller:
    def __init__(self, gui_safety_stop: Callable[[], None]):
        """
            Initialise a new mannequin Controller

            :param gui_safety_stop: function to be called when the GUI needs to be overridden because a pouch has been inflating or deflating for too long.
        """
        self.inflate_pump = Pump(_INFLATE_PUMP_PORT, 0)
        self.deflate_pump = Pump(_DEFLATE_PUMP_PORT, 0)
        self.pump_valve = Pump_valve(_PUMP_VALVE_PORT, "pump_valve")
        self.pouches = {
            'cube':            Pouch("cube", 100, 100, 5, 3),
            'thick sleeve':    Pouch("thick_sleeve", 100, 80, 4, 3),
            'cylinder':        Pouch("cylinder", 50, 50, 2, 3),
            'cylinder sleeve': Pouch("cylinder_sleeve", 75, 60, 7, 3),
            'thiccc_thigh':    Pouch("thiccc_thigh", 100, 60, 1, 3),
            'calf':            Pouch("calf", 60, 60, 3, 1),
        }

        # for monitoring which pouches are inflating/deflating
        self.inflating_pouch = None
        self.deflating_pouch = None
        self.start_time = None #time when pouch started inflating/deflating
        self.timer = None

        self.gui_safety_stop = gui_safety_stop # function to call to emergency override the UI
    
    def get_pouch(self, pouch_name:str) -> Pouch:
        if pouch_name in self.pouches:
            return self.pouches[pouch_name]

    def can_start_pump(self) -> bool:
        """
            :return whether any pouches are currently being inflated or deflated
        """
        if self.inflating_pouch != None:
            print("Must stop inflating pouch {} before inflating another.".format(self.deflating_pouch.name))
            return False
        elif self.deflating_pouch != None:
            print("Must stop deflating pouch {} before inflating another.".format(self.inflating_pouch.name))
            return False
        
        return True
    
    def inflate_pouch(self, pouch_name:str) -> bool:
        """
            Opens valve configuration for this pouch and starts the inflate pump and
            starts a countdown timer which will trigger an emergency shutoff of the pumps if 
            the pouche's max time for inflating is exceeded.

            :param pouch_name: the name of the pouch that should be inflated
            :return: whether inflating was activated successfully or not 
        """
        pouch = self.get_pouch(pouch_name)

        if not pouch:
            print("Invalid pouch id:", pouch_name)
            return False
        
        if not self.can_start_pump():
            return False
        
        self.inflating_pouch = pouch

        # open correct valves
        self.pump_valve.open_inflate()
        self.inflate_pump.set_speed(self.inflating_pouch.inflate_speed)
        self.inflate_pump.run()
        self.inflating_pouch.open_valve()

        self.start_waiting_for_stop(self.inflating_pouch.get_inflate_left())

        print("Started inflating {}".format(self.inflating_pouch.name))
        return True
    
    def stop_inflate(self) -> bool:
        """
            Stops inflating the current pouch and updates its inflate status to reflect the
            amount of time that it has been inflating for.

            :return: whether anything stopped inflating
        """
        if not self.inflating_pouch:
            print("No pouch inflating")
            return False
        
        # close valves and stop pumps
        self.inflating_pouch.close_valve()
        self.inflate_pump.stop()
        
        # update the pouche's inflate status
        time_elapsed = self.stop_timer()
        self.inflating_pouch.update_inflate_status(time_elapsed)
        
        print("Stopped inflating {}".format(self.inflating_pouch.name))
        self.inflating_pouch = None

        return True
    
    def deflate_pouch(self, pouch_name:str) -> bool:
        """
            Opens valve configuration for this pouch and starts the deflate pump and
            starts a countdown timer which will trigger an emergency shutoff of the pumps if 
            the pouche's max time for inflating is exceeded.

            :param pouch_name: the name of the pouch that should be deflated
            :return: whether deflating was activated successfully or not 
        """
        pouch = self.get_pouch(pouch_name)

        if not pouch:
            print("Invalid pouch id:", pouch_name)
            return False

        if not self.can_start_pump():
            return False

        self.deflating_pouch = pouch

        # open correct valves
        self.pump_valve.open_deflate()
        self.deflate_pump.set_speed(self.deflating_pouch.deflate_speed)
        self.deflate_pump.run()
        self.deflating_pouch.open_valve()

        self.start_waiting_for_stop(self.deflating_pouch.get_deflate_left())

        print("Started deflating {}".format(self.deflating_pouch.name))

        return True
    
    def stop_deflate(self) -> bool:
        """
            Stops deflating the current pouch and updates its inflate status to reflect the
            amount of time that it has been deflating for.

            :return: whether anything stopped deflating
        """
        if not self.deflating_pouch:
            print("No pouch deflating")
            return False

        # close valves and stop pumps
        self.deflating_pouch.close_valve()
        self.deflate_pump.stop()

        # udpate the pouche's inflate status
        time_elapsed = self.stop_timer()
        self.deflating_pouch.update_inflate_status(-time_elapsed)

        print("Stopped deflating {}".format(self.deflating_pouch.name))
        self.deflating_pouch = None

        return True
    
    def start_waiting_for_stop(self, max_time:float) -> None:
        """
            Starts a concurrent timer which will emergency stop the pumps once max_time has passed
            and record the time at which the timer was started

            :param max_time: the number of seconds after which the timer should trigger the emergency stop
        """
        self.timer = Timer(max_time, self.emergency_stop_pumps)
        self.timer.start()
        self.start_time = time()
    
    def stop_timer(self) -> float:
        """
            If a timer is running, that is stopped and the time elapsed since it started running is returned

            :return: the number of seconds that have elapsed since the timer was started
        """
        time_elapsed = time()-self.start_time
        if self.timer:
            self.timer.cancel()
            self.time = None
        return time_elapsed

    def emergency_stop_pumps(self) -> None:
        """
            Function called by the Timer when time has run out and the pouch should no longer be 
            inflated/deflated any further
        """
        if self.inflating_pouch:
            print("Emergency stop inflating")
            self.stop_inflate()
        elif self.deflating_pouch:
            print("Emergency stop deflating")
            self.stop_deflate()
        else:  # emergency stop was triggered when nothing is being
            print("Emergency stop called when no pumps are on")
            return

        self.gui_safety_stop()
    
    def reset_pouch(self, pouch: Pouch) -> None:
        """
            Deflates/Inflates the given pouch until it is in a neutral position (inflate status 0)

            :param pouch: the Pouch that needs to be reset
        """
        time_left = pouch.inflate_status
        if time_left > 0:
            self.deflate_pouch(pouch.name)
            sleep(time_left)
            self.stop_deflate()
        else:
            self.inflate_pouch(pouch.name)
            sleep(-time_left)
            self.stop_inflate()
        
        pouch.inflate_status = 0
    
    def cleanup(self):
        """
            Make sure all the pouches and pumps are reset and valves are in 
            neutral position before shutting off
        """
        self.stop_inflate()
        self.stop_deflate()

        for (_, pouch) in self.pouches:
           self.reset_pouch(pouch) 
           pouch.reset_valve()

        self.pump_valve.reset()