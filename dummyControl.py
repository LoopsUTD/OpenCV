import step as motor
import sys
from pynput import keyboard
from multiprocessing import Queue


def on_press(key):
    global stop
    stop=1
    try:
        stop=1
        print('alphanumeric key {0} pressed'.format(
                                    key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    print('{0} released'.format( 
         key))
    if key == keyboard.Key.esc:                                                      # Stop listener 
        return False
# Collect events until released



if __name__ == '__main__':
    from sys import argv
    mode=int(argv[1])
    desiredpos=int(argv[2])
    print ('{}{}'.format('mode: ',mode))
    motor.setpins(29,31)
    if (mode==0):
        print('{}{}'.format("Stepping to ",desiredpos))
        motor.step(desiredpos) 
    if (mode==1):

         
        while(True):
            global stop
            stop=0
            with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
                    listener.join()
            print(stop)
            if(stop!=1):
                motor.step(-100)
    motor.GPIO.cleanup()
