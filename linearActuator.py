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
        self.home=(self.bottom+self.top)/2
        self.moveTo(self.home)
    
        print('{}{}{}{}'.format('Bottom: ', self.bottom,'\nTop: ', self.top))

    
    def manualAdjust(self,stepSize):
        root = Tk()
        def moveUp(event):
            self.moveTo(self.current+stepSize)
        def moveDown(event):
            self.moveTo(self.current-stepSize)
        def setHome(event):
            self.home=self.current
        
        frame = Frame(root,width=100,height=100)
        label = Label(root,text='Move with arrow keys, Press space to set home.')
        label.pack()
        frame.bind('<Up>', moveUp)
        frame.bind('<Down>', moveDown)
        frame.bind('<space>', setHome)
        frame.focus_set()
        frame.pack()
        root.mainloop()
    
    def moveIntoPath(self):
        self.moveTo(self.home)
    def moveOutOfPath(self):
        self.moveTo(self.bottom+100)
    

if __name__ == "__main__":
    actuator=LinearActuator()
    actuator.findLimits()
    actuator.manualAdjust(stepSize=100)
    actuator.moveIntoPath()
    actuator.moveOutOfPath()
    actuator.moveIntoPath()
