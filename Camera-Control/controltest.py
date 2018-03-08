
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

picID = "PiShots"

triggerCommand = ["--capture-image-and-download"]

folder_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
save_location = "/home/pi/Desktop/Gphoto/images/" + folder_name
secondary_location = "/home/pi/Desktop/Gphoto/images/" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def createSaveFolder():
    try:
        os.makedirs(save_location)
        os.chdir(save_location)
    except:
        os.makedirs(secondary_location)
        print("Created new Folder.")
        os.chdir(secondary_location)

def captureImages():
    print("Try")
    gp(triggerCommand)
    print("Downloaded")

def renameImages(ID):
    for filename in os.listdir("."):
        if len(filename) < 14:
            if filename.endswith(".jpg"):
                os.rename(filename, (datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ID + ".jpg"))
                print("Renamed the JPG.")
            elif filename.endswith(".arw"):
                os.rename(filename, (datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ID + ".arw"))
                print("Renamed the ARW.")
                
createSaveFolder()
while True:
    captureImages()
    renameImages(picID)