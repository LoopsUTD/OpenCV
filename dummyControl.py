import step as motor
import sys
from pynput import keyboard
from multiprocessing import Queue
import threading

def on_press(key):
    try:
        global stop
        if key.char=='w':
            stop=-10
            return False
        if key.char=='s':
            stop=10
            return False
    except AttributeError:
        if key==keyboard.Key.down:
            stop=1
            return False
        if key==keyboard.Key.up:
            stop=-1
            return False
        print('special key {0} pressed'.format(key))

def on_release(key):
    try:
        global stop
        if key == keyboard.Key.esc:                                             
            stop=99
            return False
    except AttributeError:
        print('special key {0} pressed'.format(key))


def moveTo(target):
    global current
    current=0
    motor.step(target-current)
    current=target

if __name__ == '__main__':
    from sys import argv
    mode=int(argv[1])
    print ('{}{}'.format('mode: ',mode))
    motor.setpins(29,31)
    if (mode==0):
        desiredpos=int(argv[2])
        print('{}{}'.format("Stepping to ",desiredpos))
        motor.step(desiredpos) 
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
                motor.step(stop*100)
            
    motor.GPIO.cleanup()
