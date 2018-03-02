import RPi.GPIO as GPIO
import time
class StepperMotor:
    
    def __init__(self,stepPin,dirPin, limit1, limit2):
        self.stepPin = stepPin
        self.dirPin = dirPin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.stepPin,GPIO.OUT)
        GPIO.setup(self.dirPin,GPIO.OUT)
        self.lim1=limit1
        self.lim2=limit2
        GPIO.setup(self.lim1,GPIO.IN)
        GPIO.setup(self.lim2,GPIO.IN)
    

    def step(self,steps):
        
        stepsTaken = 0
        if steps<0:
            GPIO.output(self.dirPin,GPIO.LOW)
            limit=self.lim1
        if steps>0:
            limit=self.lim2
            GPIO.output(self.dirPin,GPIO.HIGH)
        while stepsTaken<abs(steps):
            if GPIO.input(limit)==1:
                GPIO.output(self.stepPin,GPIO.HIGH)
                time.sleep(.0000050)
                GPIO.output(self.stepPin,GPIO.LOW)
                time.sleep(.00005)
            stepsTaken = stepsTaken +1  

        GPIO.output(self.stepPin,GPIO.LOW)
    
if __name__ == "__main__":
    motor = stepperMotor(29,31,5,3)
    motor.step(3200)
    motor.step(-3200)
    time.sleep(1)
    GPIO.cleanup()
