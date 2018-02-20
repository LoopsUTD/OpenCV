import RPi.GPIO as GPIO
import time

def setpins():
    stepPin = 29
    dirPin = 31
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(stepPin,GPIO.OUT)
    GPIO.setup(dirPin,GPIO.OUT)
    
def step(steps,stepPin,dirPin):
    stepsTaken = 0
    if steps<0:
        GPIO.output(dirPin,GPIO.LOW)
    if steps>0:
        GPIO.output(dirPin,GPIO.HIGH)
    while stepsTaken<abs(steps):
        GPIO.output(stepPin,GPIO.HIGH)
        time.sleep(.0000050)
        GPIO.output(stepPin,GPIO.LOW)
        time.sleep(.00005)
        stepsTaken = stepsTaken+1
    GPIO.output(stepPin,GPIO.LOW)
    
if __name__ == "__main__":
    setpins()
    step(3200,29,31)
    step(-3200,29,31)
    time.sleep(1)
    GPIO.cleanup()
