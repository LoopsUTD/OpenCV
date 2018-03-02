import stepperMotor
import sys
from tkinter import *

class LinearActuator:
    def __init__(self):
        self.motor=stepperMotor.StepperMotor(29,31,5,3)
        self.home=0
        self.current=self.home
        self.goal=self.home
    
    def moveTo(self,target):
        success=self.motor.step(target-self.current)
        self.current=target
        return success
    def findLimits(self):
        success=self.moveTo(self.current)
        while(success):
            success=self.moveTo(self.current-1)
        self.current=0
        self.bottom=self.current

        success= self.moveTo(self.bottom+1000)
        while(success):
            success=self.moveTo(self.current+1)
            self.top=self.current
        self.middle=(self.bottom+self.top)/2
        self.moveTo(self.middle)
    
        print('{}{}{}{}'.format('Bottom: ', self.bottom,'\nTop: ', self.top))


if __name__ == "__main__":
    root =  Tk()
    actuator=LinearActuator()
    actuator.findLimits()
    def leftKey(event):
        print("Left key pressed")
        actuator.moveTo(actuator.current+100)
        
     
    def rightKey(event):
        print("Right key pressed")
        actuator.moveTo(actuator.current-100)
    frame = Frame(root, width=100, height=100)
    frame.bind('<Left>', leftKey)
    frame.bind('<Right>', rightKey)
    frame.focus_set()
    frame.pack()
    #root.mainloop()


