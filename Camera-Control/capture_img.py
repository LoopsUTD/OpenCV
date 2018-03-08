from time import sleep
from datetime import datetime
import gphoto2 as gp
import signal, os, subprocess

#kill processgphoto2
def killgphoto2Process():
    #p = subprocess.Popen(['ps', '-A'], (stdout = subprocess.PIPE)
    #out, err= p.communicate()
                         
        # line in out.splitlines():
         #                if b'gvfsd-gphoto2' in line:
          #               pid = int(line.split(None,1) [0])
           #              os,kill (pid, signal.SIGKILL)
    gp(["--summary"]) #output summary
    gp(["--show-preview"])
    sleep(10) #view the image                        
    picID= "Image"

    clearCom = ["--folder", "location of memorycard", "-R", "--delete-all-files"]
    triggerCom = ["--Trigger-capture"]
    downloadCom = ["--get-all-files"]
                         
    folder = shot_date + picID
    save_loc = "location of save" + folder

def createFolder():  #make folder to store
    try:
        os.makedirs(save_loc)
    except:
        print("Already have one")
        os.chdir(save_loc)
                         
def capture():
    gp(triggerCom)
    sleep(5)
    gp(downloadCom)
    gp(clearCom)
                         
def renamefiles(ID):
    shot_date = datetime.now().strftime("%Y-%m-%d")
    shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")                         
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG!")
            elif filename.endswith(".RAW"):
                os.rename(filename, (shot_time + ID + ".RAW"))
                print("Renamed the RAW!")     

##Main function happens here
killgphoto2Process()                                         
gp(clearCom)
                                         
while True:                                         
    createFolder()
    capture()
    renamefiles(picID)
    sleep(10)                                     