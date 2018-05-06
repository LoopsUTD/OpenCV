import RPi.GPIO as GPIO
import time
"""
Low level control for stepper motor. Directly reads and writes to GPIO pins on the Raspberry Pi (RPi). 
Can be instantiated as a stepper motor object in other files (LinearActuator.py in this project).

"""
#INPUT: 5 pins outlining the stepper motor leads, limit switches and eStop connection
#OUTPIT: Physical motion of the stepper motor
class StepperMotor:

	#StepPin: Pin to send signal to pulse pin on stepper driver
	#dirPin: Pin to send signal to dir pin on stepper driver
	#lim1: Pin to read limit swtich 1
	#lim2: Pin to read limit switch 2
	#eStop: Pin to read emergency stop
	def __init__(self,stepPin,dirPin, limit1, limit2, eStop):
		self.stepPin = stepPin
		self.dirPin = dirPin
		self.eStop = eStop
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.stepPin,GPIO.OUT)
		GPIO.setup(self.dirPin,GPIO.OUT)
		GPIO.setup(self.eStop,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		self.lim1=limit1
		self.lim2=limit2
		GPIO.setup(self.lim1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.lim2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

	def step(self,steps):
		if GPIO.input(self.eStop)==0:
			stepsTaken = 0
			if steps<0:
				GPIO.output(self.dirPin,GPIO.LOW)
				limit=self.lim1
			if steps>0:
				limit=self.lim2
				GPIO.output(self.dirPin,GPIO.HIGH)
			while stepsTaken<abs(steps):
				print(GPIO.input(limit))
				if GPIO.input(limit)==0:
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
	motor = StepperMotor(11,15,37,33,31)
	motor.step(3200)
	motor.step(-3200)
	time.sleep(1)
	GPIO.cleanup()
