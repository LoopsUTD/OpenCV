import tkinter as tk
from PIL import Image, ImageTk
import traceback

class FullScreenApp(object):
    def __init__(self, master, images = None, **kwargs):
        self.master=master
        pad=3
        self.images = images
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        master.bind('<space>', self.nextImage)
        image = Image.open('test.jpg')
        photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(image=photo)
        self.label.image = photo
        self.label.pack()
        #image = Tk.PhotoImage(file='test.png')            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def nextImage(self, event):
        try:
            print("I am trying to activate")
            photo = ImageTk.PhotoImage(Image.open(self.images[1]))
            self.label.config(image=photo)
            self.label.image = photo
            self.label.pack()
        except Exception:
            traceback.print_exc()
            return


root=tk.Tk()
app=FullScreenApp(root, ['test.jpg', 'second.jpg'])
root.mainloop()