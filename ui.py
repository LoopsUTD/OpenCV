#python3.6

import readline
import argparse
import logging
import sys #this gets you commandline args
import traceback
from linearActuator import LinearActuator
from cameraHandling import Camera
from displayHandling import FullScreenApp
from TestHandler import TestHandler
import tkinter as tk


log = logging.getLogger(__name__)
VERSION = "0.4a"
numLensToTest = 1
DefaultOutputFolder = "RAW/"
mainDisplay = None

#numOptionsInMenu = 4
#KEEPGOING = True

def main():
	##Shit globals that need to be resolved
	#DefaultOutputFolder = "RAW/"
	#mainDisplay = None
	#root = tk.Tk()
	#FullScreenApp.getInstance()

	##LOGGING
	loggingLevel = logging.DEBUG
	log.setLevel(loggingLevel)
	handler = logging.StreamHandler()
	handler.setLevel(loggingLevel)
	#format = logging.Formatter('%(name)s -- %(levelname)s -- %(message)s')
	format = logging.Formatter('%(levelname)s -- %(message)s')
	handler.setFormatter(format)
	log.addHandler(handler)

	##INPUT PARSING
	parser = argparse.ArgumentParser()
	parser.add_argument("-V", "--Version", action='version', version =('%(prog)s {}').format(VERSION), help="returns version number")
	#TODO: Decrease default verbosity to a lower number
	parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output Verbosity (max 3)")
	parser.add_argument("-t", "--tests", help="link to test images")
	args = parser.parse_args()

	if args.verbose >= 3:
		loggingLevel = logging.DEBUG
	elif args.verbose >= 2:
		loggingLevel = logging.INFO
	elif args.verbose >= 1:
		loggingLevel = logging.WARNING
	else:
		#loggingLevel = logging.ERROR
		#TODO: Comment out the below section for production code, uncomment the above
		loggingLevel = logging.DEBUG

	log.setLevel(loggingLevel)

	log.debug("Logger log is setup with logging level: %d" % loggingLevel)
	log.debug("Input Args: %s" % args)
	log.debug('tests has the value: %s' % args.tests)

	## MAIN LOOP
	opts = printMainMenu()
	badSelection = True
	val = 0
	#Validate input.
	while(badSelection):
		selection = input("Enter selection [1-%d]: " % len(opts))
		log.debug("User entered %s" % selection)
		try:
			val = int(selection)
			if val not in opts:
				raise BadInputException
			opts[val]()

		except ExitException:
			log.critical("Exiting The Application.")
			if globalCamera is not None:
				globalCamera.close()
			badSelection = False
		except BadInputException:
			log.error("Invalid Input! Please Try Again or [Ctrl-c] to abort")
		except Exception:
			log.error(traceback.print_exc())

#Main Menu Options
		# #1:selectTestFileHandler, 
		# 1:setupDisplayHandler,
		# 2:adjustLinearActuatorHandler, 
		# #3:numLensToTestHandler, 
		# 3:calibrateCameraHandler, 
		# 4:checkCameraConnectionHandler, 
		# 5:takePhotoHandler,
		# 6:runTestHandler, 
		# 7:moveLinearActuatorIntoPath,
		# 8:moveLinearActuatorOutOfWay,
		# 9:exitThisProgram

	
##Why does this work? see here:
#https://stackoverflow.com/questions/10874432/possible-to-change-function-name-in-definition
def rename(newName):
	def decorator(f):
		f.__name__ = newName
		return f
	return decorator

##Why use handler functions in a Dictionary for options? See Here:
#https://stackoverflow.com/questions/3978624/since-python-doesnt-have-a-switch-statement-what-should-i-use

	#How to use tKinter without Mainloop()
	#https://gordonlesti.com/use-tkinter-without-mainloop/
	#https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop



@rename("Initialize the Display")
def setupDisplayHandler():
	log.info("initializing the Display Handler...")	
	FullScreenApp.getInstance()

@rename("Initialize Linear Actuator")
def adjustLinearActuatorHandler():
	log.info("adjusting Linear Actuator")
	
	LinearActuator.getInstance()
	#actuator.findLimits()

	#actuator.manualAdjust(stepSize = 100)
	
# @rename("Select Test File")
# def selectTestFileHandler():
# 	log.info("Selecting Test File")


#TODO: Does this need to be here?
@rename("Move Out Of Way")
def moveLinearActuatorOutOfWay():
	log.info("User Moving Linear Actuator Out of The Way")
	actuator = LinearActuator.getInstance()
	actuator.moveOutOfPath()

@rename("Move Into Way")
def moveLinearActuatorIntoPath():
	log.info("User Moving Linear Actuator into path")	
	actuator = LinearActuator.getInstance()
	actuator.moveIntoPath()


@rename("Change number of Lens to test (default: %d)" % numLensToTest)
def numLensToTestHandler():
	log.info("adjusting number of lens to test")

@rename("Calibrate Camera")
def calibrateCameraHandler(camera = None, actuator = None):
	log.info("Running Camera Calibration")
	##DAVID CODE GO HERE

	return camera, actuator


@rename("Get Camera Settings and Summary")
def checkCameraConnectionHandler():
	log.info("checking to see if camera is connected")
	camera = Camera.getInstance()
	text = camera.getCameraSummary()
	print(text)

@rename("Take Photo Menu")
def takePhotoHandler():
	testhandling = TestHandler(logLevelDefault = logging.DEBUG)
	testhandling.printMainMenu()

	badSelection = True
	while(badSelection):
		try:
			selection = input("enter selection: [1-%d] " % len(myOpts))
			val = int(selection)
			if val not in testhandling.myOpts:
				raise BadInputException
			if val == 4:
				badSelection = False

			testhandling.myOpts[val]()

		except BadInputException:
			traceback.print_exc()
			log.error("Invalid Input! Please Try Again or Enter 4 to return")


# @rename("Initialize the Display")
# def setupDisplayHandler(ROOT = None, mainDisp = None, testImages = None, camera = None, actuator = None):
# 	log.info("User is manually displaying an image")
	
# 	#How to use tKinter without Mainloop()
# 	#https://gordonlesti.com/use-tkinter-without-mainloop/
# 	#https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
# 	if mainDisp is None:
# 		#root=ROOT
		
# 		#mainDisp=FullScreenApp(ROOT, testImages) #pass images into the argument when you create this object.
# 		ROOT.update()

# 	return mainDisp
# 		#root.mainloop()

# def manualUpdateImage(mainDisplay = None, newImageFilePath = None, ROOT = None):
# 	if mainDisplay is None:
# 		raise BadInputException("Initialize the Display First!")
# 	mainDisplay.updateImage(newImageFilePath)
# 	ROOT.update()


@rename("Run Test")
def runTestHandler():
	log.info("User is trying to run the test")

@rename("Exit")
def exitThisProgram(camera=None,actuator = None):
	raise ExitException("User Wants to Exit")

def printMainMenu():
	welcome = "UTDesign Team LOOPS [547] Version: %s \n\n" % VERSION
	mainmsg = "Please select from the following options:\n"

	#Why use a Dict? Because it's so sneaky clean!!
	#See links above to see how I made this so slick.
	options = {
		#1:selectTestFileHandler, 
		1:setupDisplayHandler,
		2:adjustLinearActuatorHandler, 
		#3:numLensToTestHandler, 
		3:calibrateCameraHandler, 
		4:checkCameraConnectionHandler, 
		5:takePhotoHandler,
		6:runTestHandler, 
		7:moveLinearActuatorIntoPath,
		8:moveLinearActuatorOutOfWay,
		9:exitThisProgram
	}

	print(welcome + mainmsg)
	for key, opt in options.items():
		print("\t%d. %s" % (key, opt.__name__))


	return options

class ExitException(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self,"user wants to Exit")

class BadInputException(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self,"Invalid Input")

if __name__ == "__main__":
	main()
