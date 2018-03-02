#python3.6

import readline
import argparse
import logging
import sys #this gets you commandline args

log = logging.getLogger(__name__)
VERSION = "0.1"
numLensToTest = 3
numOptionsInMenu = 4
KEEPGOING = True

def main():
	loggingLevel = logging.DEBUG
	log.setLevel(loggingLevel)

	handler = logging.StreamHandler()
	handler.setLevel(loggingLevel)
	#format = logging.Formatter('%(name)s -- %(levelname)s -- %(message)s')
	format = logging.Formatter('%(levelname)s -- %(message)s')
	handler.setFormatter(format)

	log.addHandler(handler)


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

	opts = printMainMenu()
	badSelection = True
	val = 0
	#Validate input. TODO: Update the validation to autocheck the keys to be more efficient
	while(badSelection):
		selection = input("Enter selection [1-%d]: " % len(opts))
		log.debug("User entered %s" % selection)
		try:
			val = int(selection)
			if val<1 or val > len(opts):
				raise Exception

			#badSelection = False
			opts[val]()
		except ExitException:
			log.critical("Exiting The Application.")
			badSelection = False
		except:
			log.error("Invalid Input! Please Try Again or [Ctrl-c] to abort")

	
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
def adjustLinearActuatorHandler():
	log.info("adjusting Linear Actuator")

@rename("Change number of Lens to test (default: %d)" % numLensToTest)
def numLensToTestHandler():
	log.info("adjusting number of lens to test")

@rename("Calibrate Camera")
def calibrateCameraHandler():
	log.info("Running Camera Calibration")

@rename("Get Camera Settings and Summary")
def checkCameraConnectionHandler():
	log.info("checking to see if camera is connected")

@rename("Run Test")
def runTestHandler():
	log.info("User is trying to run the test")

@rename("Exit")
def exitThisProgram():
	raise ExitException("User Wants to Exit")

def printMainMenu():
	welcome = "UTDesign Team LOOPS [547] Version: %s \n\n" % VERSION
	mainmsg = "Please select from the following options:\n"

	#Why use a Dict? Because it's so sneaky clean!!
	#See links above to see how I made this so slick.
	options = {1: selectTestFileHandler, 2:adjustLinearActuatorHandler, 3:numLensToTestHandler, 4:calibrateCameraHandler, 5:checkCameraConnectionHandler, 6:runTestHandler, 7: exitThisProgram}

	print(welcome + mainmsg)
	for key, opt in options.items():
		print("\t%d. %s" % (key, opt.__name__))


	return options

class ExitException(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self,"user wants to Exit")

if __name__ == "__main__":
	main()
