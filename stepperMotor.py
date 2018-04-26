import RPi.GPIO as GPIO
import time
class StepperMotor:
   
	#StepPin: Pin to send signal to pulse pin on stepper driver
	#diePin: Pin to send signal to dir pin on stepper driver
	#lim1: Pin to read limit swtich 1
	#lim2: Pin to read limit switch 2
	def __init__(self,stepPin,dirPin, limit1, limit2, eStop):
		self.stepPin = stepPin
		self.dirPin = dirPin
		self.eStop = eStop
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.stepPin,GPIO.OUT)
		GPIO.setup(self.dirPin,GPIO.OUT)
		self.lim1=limit1
		self.lim2=limit2
		GPIO.setup(self.lim1,GPIO.IN)
		GPIO.setup(self.lim2,GPIO.IN)
		GPIO.setup(self.eStop,GPIO.IN)
		
	def step(self,steps):	
		if (GPIO.input(self.eStop)==1):
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
						else:
							return False
						stepsTaken = stepsTaken +1  
			GPIO.output(self.stepPin,GPIO.LOW)
			return True
		else:
			return False
	
if __name__ == "__main__":
	motor = StepperMotor(17,22,37,33,31)
	motor.step(3200)
	motor.step(-3200)
	time.sleep(1)
	GPIO.cleanup()
