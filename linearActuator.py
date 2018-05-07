import stepperMotor
import sys
from tkinter import *
import logging

"""
High level controller for linear actuator.
Manual adjustment as well as automated motion are enabled by this class.
INPUT: User controlled input
OUTPUT: commands to stepper motor
FILE I/O: logs to file for display in UI
"""
class LinearActuator(object):
    _singletonInstance = None
    #stepperMotor class from stepperMotor.py
    #home - adjustable position to return to (in steps)
    #current - current position (in steps_
    #goal - position that actuator is moving towards
    #Singleton in Python?
    #https://gist.github.com/pazdera/1098129
    @staticmethod
    def getInstance():
        """Get Instance of Singleton class"""
        if LinearActuator._singletonInstance == None:
            LinearActuator()
        return LinearActuator._singletonInstance
    def __init__(self):
        if LinearActuator._singletonInstance != None:
            raise Exception("This class is a Singleton!")
        else:
            LinearActuator._singletonInstance = self
            self.log = logging.getLogger("mainApp")
            self.log.info("Initializing the Linear Actuator...")
            self.motor=stepperMotor.StepperMotor(11,15,37,33,31)
            self.top=0
            self.bottom=0
            self.home=0
            self.current=self.home
            self.goal=self.home
            #self.bottom=-25000
            self.findLimits()
            #self.manualAdjust(stepSize = 100)
    
    #Returns boolean statement corresponding to whether goal was reached
    def moveTo(self,target):
        success,stepsTaken=self.motor.step(target-self.current)
        if (target-self.current)>0:
		self.current=self.current+stepsTaken
	else
		self.current=self.current-stepsTaken
        print(self.current)
        return success

    def findLimits(self):
            numCounts=0	
            success=self.moveTo(self.current)
            while(numCounts<50):
                success=self.moveTo(self.current-1)
                if(success==False):
                    numCounts=numCounts+1
                    self.current=0
                self.bottom=self.current
                
            numCounts=0
            #success= self.moveTo(self.bottom+1000)
            self.top=self.current
            while(numCounts<50):
                success=self.moveTo(self.current+1)
                if(success==False):
                    numCounts=numCounts+1
                self.top=self.current
                #self.home=(self.bottom+self.top)/2
            self.home=6875
            self.moveTo(self.home)
                #self.log.debug('{}{}{}{}'.format('Bottom: ', self.bottom,'\tTop: ', self.top))
    def moveUp(self,event,step):
        self.moveTo(self.current+step)

    def moveDown(self,event,step):
        self.moveTo(self.current-step)

    def setHome(self,event):
        self.home=self.current
        self.log.debug('Home Position Set: %d' % self.home)

	
    def goHome(self,event):
        self.moveTo(self.home)
	
    def manualAdjust(self,stepSize):
        try: 
            root = Tk()
            frame = Frame(root,width=100,height=100)
            label = Label(root,text='Move with arrow keys, Press x to set home. Press space to got home.')
            label.pack()
            quitBtn = Button(root, text="Quit", command=root.destroy)
            quitBtn.pack()
            frame.bind('<Up>', lambda event: self.moveUp(event,stepSize/10)  )
            frame.bind('<Down>', lambda event: self.moveDown(event,stepSize/10))
            frame.bind('<w>', lambda event: self.moveUp(event,stepSize)  )
            frame.bind('<s>', lambda event: self.moveDown(event,stepSize))
            frame.bind('<x>', self.setHome)
            frame.bind('<a>', lambda event: self.moveTo(self.top))
            frame.bind('<d>', lambda event: self.moveTo(self.bottom))
            frame.bind('<space>',self.goHome)
            frame.bind('<Return>',lambda event: root.destroy) #testing!
            frame.focus_set()
            frame.pack()
            #https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
            while(True):
                root.update()
                root.update_idletasks()
                #self.log.debug("Home Value: %d" % self.home)
        except Exception:
            return
	
    def moveIntoPath(self):
        self.moveTo(self.home)
    def moveOutOfPath(self):
        self.moveTo(self.bottom)
if __name__=='__main__':
    la=LinearActuator.getInstance()
    la.manualAdjust(100)   

