import gphoto2 as gp
import PIL
import logging
import os
import sys
import time



### Goals:
# Get Camera Config From Camera
	#use object oriented approach to list all the children in an iterable list, (I can do this!)

# Show a "Live Preview, at 10fps"
	#Help? 

# Allow user to use the keyboard to update:
	#Exposure (e to incr, E to decr)
	#ISO (i to incr, I to decr)
	#Apeture (a to incr, A to decr)
	#Pull this from an enumerated list 

# Update the desired values (if the user chooses to save) to the camera
# Exit the Camera Configurator


def listMainSettings(args):
	camera = gp.Camera()
	camera.init()
	myConfigs = {
		'capturetarget': "",
		'iso': "",
		'f-number':"",
		'shutterspeed': "",
		'imagequality': "",
		'imagesize': ""
	}
	try:
		config = camera.get_config()
		for sections in config.get_children():
			if "settings" not in sections.get_name():
				continue
			print("\n#########{} ({})###########\n".format(sections.get_label(), sections.get_name()))
			for child in sections.get_children():
				if child.get_name() not in myConfigs:
					continue
				choicelist = []
				if child.get_type() == 5:
					for choice in child.get_choices():
						choicelist.append(choice)
				print("{} {} type:{} choices:{}".format(child.get_name(), child.get_value(), child.get_type(), choicelist))
				#else
				#for choice in 
	finally:
		camera.exit()



def listAllSettings(args):
	camera = gp.Camera()
	camera.init()
	try:	
		config = camera.get_config()

		#print out configs and their values:
		for sections in config.get_children():
			print("\n#########{} ({})###########\n".format(sections.get_label(), sections.get_name()))
			for child in sections.get_children():
				print("{} {} type:{}".format(child.get_name(), child.get_value(), child.get_type()))
	finally:
		camera.exit()

if(__name__ == "__main__"):
	listMainSettings(sys.argv[1:])