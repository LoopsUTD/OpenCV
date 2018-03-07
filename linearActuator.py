import stepperMotor
import sys
from tkinter import *

class LinearActuator:
    #stepperMotor class from stepperMotor.py
    #home - adjustable position to return to (in steps)
    #current - current position (in steps_
    #goal - position that actuator is moving towards
    def __init__(self):
        self.motor=stepperMotor.StepperMotor(29,31,5,3)
        self.home=0
        self.current=self.home
        self.goal=self.home
    
    #Returns boolean statement corresponding to whether goal was reached
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
    
    def moveUp(self,event,step):
        self.moveTo(self.current+step)

    def moveDown(self,event,step):
        self.moveTo(self.current-step)

    def setHome(self,event):
        self.home=self.current
    
    def goHome(self,event):
        self.moveTo(self.home)
    
    def manualAdjust(self,stepSize):
        root = Tk()
        frame = Frame(root,width=100,height=100)
        label = Label(root,text='Move with arrow keys, Press x to set home. Press space to got home.')
        label.pack()
        frame.bind('<Up>', lambda event: self.moveUp(event,stepSize/10)  )
        frame.bind('<Down>', lambda event: self.moveDown(event,stepSize/10))
        frame.bind('<w>', lambda event: self.moveUp(event,stepSize)  )
        frame.bind('<s>', lambda event: self.moveDown(event,stepSize))
        frame.bind('<x>', self.setHome)
        frame.bind('<space>',self.goHome)
        frame.focus_set()
        frame.pack()
        Button(root, text="Quit", command=root.destroy).pack()
        root.mainloop()
    
    def moveIntoPath(self):
        self.moveTo(self.home)
    def moveOutOfPath(self):
        self.moveTo(self.bottom+100)
    

if __name__ == "__main__":
    actuator=LinearActuator()
    actuator.findLimits()
    actuator.manualAdjust(stepSize=100)
    #actuator.moveIntoPath()
    actuator.moveOutOfPath()
    actuator.moveIntoPath()
