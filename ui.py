#python3.6
#Dhruv Narayanan
#2/19/18

import readline
import argparse
import logging
import sys #this gets you commandline args

log = logging.getLogger(__name__)
VERSION = "0.1"
numLensToTest = 3
numOptionsInMenu = 4

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
	parser.add_argument("-v", "--verbose", action="count", default=3, help="increase output Verbosity (max 3)")
	parser.add_argument("-t", "--tests", help="link to test images")
	args = parser.parse_args()

	if args.verbose >= 3:
		loggingLevel = logging.DEBUG
	elif args.verbose >= 2:
		loggingLevel = logging.INFO
	elif args.verbose >= 1:
		loggingLevel = logging.WARNING
	else:
		loggingLevel = logging.ERROR

	log.setLevel(loggingLevel)

	log.debug("Logger log is setup with logging level: %d" % loggingLevel)
	log.debug("Input Args: %s" % args)
	log.debug('tests has the value: %s' % args.tests)

	opts = printMenu()
	badSelection = True
	while(badSelection):
		selection = input("Enter selection [1-4]: ")
		log.debug("User entered %s" % selection)
		try:
			val = int(selection)
			if val<1 or val > len(opts):
				raise Exception

			badSelection = False
		except:
			log.error("Invalid Input! Please Try Again or [Ctrl-c] to abort")



def printMenu():
	welcome = "UTDesign Team LOOPS [547] Version: %s \n\n" % VERSION
	mainmsg = "Please select from the following options:\n"
	option1 = "\t1. Select Test File\n"
	option2 = "\t2. Adjust Linear Actuator\n"
	option3 = "\t3. Change number of Lens to test (default: %d)\n" % numLensToTest
	option4 = "\t4. Test\n"

	options = [option1,option2,option3,option4]

	print(welcome + mainmsg + option1 + option2 + option3 + option4)

	return options

if __name__ == "__main__":
	main()