from threading import Thread
from time import sleep, time

global keep_going
global threadd

global start_time

def starter():
    global start_time
    start_time = time()
    threadd.start()
    sleep(2)
    stopper()

def stopper():
    global keep_going
    print("stopping thead")
    keep_going = False
    threadd.join()
    print("stopped by stopper")

def after_stopped():
    print("stopped by thread")

def do_something():
    while conditional() and keep_going:
        print("doing something")
        sleep(1)
    
    print("thread stopping")
    if keep_going:
        after_stopped()

def conditional():
    return time()-start_time < 5

if __name__=="__main__":
    keep_going = True
    threadd = Thread(target=do_something)
    starter()