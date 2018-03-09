#python3.6

import readline
import argparse
import logging
import sys #this gets you commandline args
import traceback
from linearActuator import LinearActuator
from cameraHandling import Camera
import displayHandling

log = logging.getLogger(__name__)
VERSION = "0.2"
numLensToTest = 1
DefaultOutputFolder = "RAW/"
mainDisplay = None
#numOptionsInMenu = 4
#KEEPGOING = True

def main():
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


	linActuator = None
	globalCamera = None
	


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
			globalCamera, linActuator = opts[val](globalCamera,linActuator) #runs the correct handler function
		except ExitException:
			log.critical("Exiting The Application.")
			if globalCamera is not None:
				globalCamera.close()
			badSelection = False
		except BadInputException:
			log.error("Invalid Input! Please Try Again or [Ctrl-c] to abort")
		except Exception:
			log.error(traceback.print_exc())

	
##Why does this work? see here:
#https://stackoverflow.com/questions/10874432/possible-to-change-function-name-in-definition
def rename(newName):
	def decorator(f):
		f.__name__ = newName
		return f
	return decorator

##Why use handler functions in a Dictionary for options? See Here:
#https://stackoverflow.com/questions/3978624/since-python-doesnt-have-a-switch-statement-what-should-i-use
@rename("Select Test File")
def selectTestFileHandler():
	log.info("Selecting Test File")

@rename("Adjust Linear Actuator")
def adjustLinearActuatorHandler(camera = None, actuator = None):
	log.info("adjusting Linear Actuator")
	if actuator is None:
		actuator = LinearActuator()
		actuator.findLimits()

	actuator.manualAdjust(stepSize = 100)
	return camera, actuator

#TODO: Does this need to be here?
@rename("Move Out Of Way")
def moveLinearActuatorOutOfWay(camera = None, actuator = None):
	if actuator is None:
		adjustLinearActuatorHandler(camera,actuator)
	actuator.moveOutOfPath()
	return camera, actuator

@rename("Move Into Way")
def moveLinearActuatorIntoPath(camera = None, actuator = None):
	if actuator is None:
		adjustLinearActuatorHandler(camera,actuator)
	actuator.moveIntoPath()
	return camera, actuator

@rename("Change number of Lens to test (default: %d)" % numLensToTest)
def numLensToTestHandler():
	log.info("adjusting number of lens to test")

@rename("Calibrate Camera")
def calibrateCameraHandler(camera = None, actuator = None):
	log.info("Running Camera Calibration")

@rename("Get Camera Settings and Summary")
def checkCameraConnectionHandler(camera = None, actuator = None):
	log.info("checking to see if camera is connected")
	if camera is None:
		camera = Camera()

	text = camera.getCameraSummary()
	print(text)
	return camera, actuator

@rename("Take Photo")
def takePhotoHandler(camera, actuator = None):
	if camera is None:
		camera = Camera()

	print("Current Output folder is: %s" % DefaultOutputFolder)
	print("Current test images are: %s" % args.tests)
	print("Please Select from the following options:\n")
	myOpts = {
		1:"Take Photo With First Test Image",
		2:"Change Output folder",
		3:"Take Photo with other test image",
		4:"Return to Main Menu"
	}
	for key, opt in myOpts.items():
		print("\t%d. %s" % (key, opt))

	badSelection = True
	while(badSelection):
		try:
			selection = input("enter selection: [1-%d]" % len(myOpts))
			val = int(selection)
			if val not in myOpts:
				raise BadInputException
			if val == 1:
				if len(args.tests) > 0:
					log.info("user is taking image at: %s" % DefaultOutputFolder)
					manualUpdateImage(args.tests[0])
					target = camera.takePhoto(foldername = DefaultOutputFolder)
					log.info("Image saved at: %s" % target)
				else:
					print("no default test images defined!")
			if val == 2:
				newFolderNameRaw = input("Enter new folder name: ")
				strippedName = newFolderNameRaw.strip()
				nameWithSlashes = strippedName.replace(' ', '')
				goodName = nameWithSlashes.replace('\\', '')
				betterName = goodName.replace("\'", '')
				bestName = betterName.replace('\"', '')
				DefaultOutputFolder = bestName
				print("Updated Output folder is: %s" % DefaultOutputFolder)
			if val == 3:
				newImagePath = input("enter test image path and file name: (must be exact!)")
				log.info("user is taking image at %s with %s" % (DefaultOutputFolder, newImagePath))
				manualUpdateImage(newImagePath)
				target = camera.takePhoto(foldername = DefaultOutputFolder)
					log.info("Image saved at: %s" % target)

			if val == 4:
				badSelection = False
		except BadInputException:
			log.error("Invalid Input! Please Try Again or Enter 4 to return")

	#camera.takePhoto(folderName = DefaultOutputFolder)

	return camera, actuator

@rename("Initialize the Display")
def setupDisplayHandler(camera = None, actuator = None):
	log.info("User is manually displaying an image")
	if mainDisplay is None:
		root=tk.Tk()
		mainDisplay=FullScreenApp(root, args.tests) #pass images into the argument when you create this object.
		root.mainloop()

def manualUpdateImage(newImageFilePath):
	if mainDisplay is None:
		raise BadInputException("Initialize the Display First!")
	mainDisplay.updateImage(newImageFilePath)


@rename("Run Test")
def runTestHandler():
	log.info("User is trying to run the test")

@rename("Exit")
def exitThisProgram(camera=None,act = None):
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