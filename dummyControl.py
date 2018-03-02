import stepperMotor as motor
import sys
from pynput import keyboard
from multiprocessing import Queue
import threading

def on_press(key):
    try:
        global stop
        global goal
        global home
        global current
        if key.char=='w':
            stop=-10
            
            return False
        if key.char=='s':
            stop=10
            return False
        if key.char=='x':
            stop=11
            home=current
            return False
    except AttributeError:
        if key==keyboard.Key.down:
            stop=1
            return False
        if key==keyboard.Key.up:
            stop=-1
            return False
        if key == keyboard.Key.space:
            goal=home
            stop=11
            return False
        

def on_release(key):
        global current
        global home
        global stop
        if key == keyboard.Key.esc:                                             
            stop=99
            return False


def moveTo(target):
    global current
    motor.step(target-current)
    current=target

if __name__ == '__main__':
    from sys import argv
    mode=int(argv[1])
    print ('{}{}'.format('mode: ',mode))
    motor=motor.stepperMotor(29,31)
    global current
    global home
    global goal
    home=0
    current=home
    goal=current
    if (mode==0):
        goal=int(argv[2])
        print('{}{}'.format("Stepping to ",goal))
        moveTo(goal) 
    if (mode==1):
        global stop
        adjust=True
        while(adjust==True):
            stop=0
            with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
                    listener.join()
            if(stop==99):
                adjust=False
            if(abs(stop)<=10):
                goal=current+stop*100
            print(goal)
            moveTo(goal)
            
    motor.GPIO.cleanup()
