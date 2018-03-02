import RPi.GPIO as GPIO
import time
class stepperMotor:
    
    def __init__(self,stepPin,dirPin):
     self.stepPin = stepPin
     self.dirPin = dirPin
     GPIO.setmode(GPIO.BOARD)
     GPIO.setup(self.stepPin,GPIO.OUT)
     GPIO.setup(self.dirPin,GPIO.OUT)
    
    def step(self,steps):
     stepsTaken = 0
     if steps<0:
         GPIO.output(self.dirPin,GPIO.LOW)
     if steps>0:
         GPIO.output(self.dirPin,GPIO.HIGH)
     while stepsTaken<abs(steps):
         GPIO.output(self.stepPin,GPIO.HIGH)
         time.sleep(.0000050)
         GPIO.output(self.stepPin,GPIO.LOW)
         time.sleep(.00005)
         stepsTaken = stepsTaken +1  
     GPIO.output(self.stepPin,GPIO.LOW)
    
if __name__ == "__main__":
    motor = stepperMotor(29,31)
    motor.step(3200)
    motor.step(-3200)
    time.sleep(1)
    GPIO.cleanup()
