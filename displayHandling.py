import tkinter as tk
from PIL import Image, ImageTk
import traceback
import logging

class FullScreenApp(tk.Tk):
    _singletonInstance = None
    
    @staticmethod
    def getInstance(inputImages=None):
        if FullScreenApp._singletonInstance == None:
            FullScreenApp(images=inputImages)
        
        return FullScreenApp._singletonInstance

    def __init__(self, images=None, *args, **kwargs):
        if FullScreenApp._singletonInstance != None:
            raise Exception("This is a singleton Instance")
        else:
            FullScreenApp._singletonInstance = self
            self.log = logging.getLogger("mainApp")
            self.log.debug("Initializing FullScreenApp...")
            self.master = tk.Tk()
            pad=0
            self.images = images
            self._geom='200x200+0+0'
            self.master.geometry("{0}x{1}+0+0".format(
                self.master.winfo_screenwidth()-pad, self.master.winfo_screenheight()-pad))
            self.master.bind('<Escape>',self.toggle_geom)
            self.label = tk.Label()
            if self.images is not None:
                image = Image.open(self.images[0])
                photo = ImageTk.PhotoImage(image)
                self.label.config(image=photo)
                self.label.image = photo
                self.label.pack()
                self.master.update()
            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        self.log.debug(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def updateImage(self, newImageFilePath):
        try:
            self.log.info("Updating Image...")
            photo = ImageTk.PhotoImage(Image.open(newImageFilePath))
            self.label.config(image=photo)
            self.label.image = photo
            self.label.pack()
            self.master.update()
        except Exception:
            self.log.error("Error - maybe bad image File path?")
            traceback.print_exc()
            return
