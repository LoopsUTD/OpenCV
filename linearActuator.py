import stepperMotor
import sys
from tkinter import *

class LinearActuator:
    def __init__(arg):
        self.data=arg



if __name__ == "__main__":
    root =  Tk()
    def leftKey(event):
        print("Left key pressed")
     
    def rightKey(event):
        print("Right key pressed")
             
    frame = Frame(root, width=100, height=100)
    frame.bind('<Left>', leftKey)
    frame.bind('<Right>', rightKey)
    frame.focus_set()
    frame.pack()
    root.mainloop()


