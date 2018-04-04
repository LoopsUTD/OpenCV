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


log = logging.getLogger("mainApp")
VERSION = "0.6"
numLensToTest = 1
DefaultOutputFolder = "RAW/"
mainDisplay = None

def main():

	##LOGGING
	loggingLevel = logging.DEBUG
	log.setLevel(loggingLevel)
	handler = logging.StreamHandler()
	handler.setLevel(loggingLevel)
	#format = logging.Formatter('%(name)s -- %(levelname)s -- %(message)s')
	format = logging.Formatter('%(module)s -- %(levelname)s -- %(message)s')
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
			Camera.getInstance().close()
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
	
	actuator = LinearActuator.getInstance()
	
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
def calibrateCameraHandler():
	log.info("Running Camera Calibration")
	##DAVID CODE GO HERE
	camera = Camera.getInstance()
	actuator = LinearActuator.getInstance()
	


@rename("Get Camera Settings and Summary")
def checkCameraConnectionHandler():
	log.info("checking to see if camera is connected")
	camera = Camera.getInstance()
	text = camera.getCameraSummary()
	print(text)

@rename("Testing Menu")
def takePhotoHandler():
	testhandling = TestHandler(logLevelDefault = logging.DEBUG)
	testhandling.printMainMenu()

	badSelection = True
	while(badSelection):
		try:
			selection = input("enter selection: [1-%d] " % len(testhandling.myOpts))
			val = int(selection)
			if val not in testhandling.myOpts:
				raise BadInputException
			if val == len(testhandling.myOpts): #ASSUME LAST OPTION IS EXIT
				badSelection = False

			testhandling.myOpts[val]()

		except BadInputException:
			traceback.print_exc()
			log.error("Invalid Input! Please Try Again or Enter %d to return" % len(testhandling.myOpts))


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
	# options = {
	# 	#1:selectTestFileHandler, 
	# 	1:setupDisplayHandler,
	# 	2:adjustLinearActuatorHandler, 
	# 	#3:numLensToTestHandler, 
	# 	3:calibrateCameraHandler, 
	# 	4:checkCameraConnectionHandler, 
	# 	5:takePhotoHandler,
	# 	6:runTestHandler, 
	# 	7:moveLinearActuatorIntoPath,
	# 	8:moveLinearActuatorOutOfWay,
	# 	9:exitThisProgram
	# }
	options = {
		1: takePhotoHandler,
		2: calibrateCameraHandler,
		3: exitThisProgram
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
