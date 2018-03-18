import tkinter as tk 
import logging
import os
import subprocess
import sys
import time

import gphoto2 as gp
from linearActuator import LinearActuator
from cameraHandling import Camera
from displayHandling import FullScreenApp


class TestHandler():
	def __init__(self, testImages = None, defOutFolder = None, logLevelDefault = None):
		self.log = logging.getLogger(__name__)
		handler = logging.StreamHandler()
		if logLevelDefault is None:
			handler.setLevel(logging.INFO)
		else:
			handler.setLevel(logLevelDefault)
		format = logging.Formatter('%(levelname)s -- %(message)s')
		handler.setFormatter(format)
		self.log.addHandler(handler)
		self.log.info("Initializing Test Handler")

		#Set Default variables:
		if testImages is None:
			self.testImages = ['test.jpg']
		else:
			self.testImages = testImages

		if defOutFolder is None:
			self.defOutFolder = "RAW/"
		else:
			self.defOutFolder = defOutFolder

		#Initialize Singleton Variables and store a memory pointer in this object.
		self.camera = Camera()
		self.actuator, firstTime = LinearActuator() #This should already have been initialized, but it will re-initialize if it hasn't been.
		self.display = FullScreenApp()

	def printMainMenu(self):
		print("Current Output folder is: %s" % self.defOutFolder)
		print("Current test image is: %s" % self.testImages)
		print("Please Select from the following options:\n")
		self.myOpts = {
			1:self.takePhotoNow,
			2:self.changeOutputFolder,
			3:self.takePhotoOtherImage,
			4:self.exit
		}
		for key, opt in self.myOpts.items():
			print("\t%d. %s" % (key, opt))



	#@rename("Take Photo With First Test Image")
	def takePhotoNow(self):
		self.log.info("user is storing image in: %s with test photo: %s" % (self.defOutFolder, self.testImages))
		self.display.updateImage(self.testImages[0])
		target = self.camera.takePhoto(folderName = self.defOutFolder)
		self.log.info("photo saved at: %s" % target)

	def changeOutputFolder(self):
		newFolderNameRaw = input("Enter new folder name: ")
		strippedName = newFolderNameRaw.strip()
		nameWithSlashes = strippedName.replace(' ', '')
		goodName = nameWithSlashes.replace('\\', '')
		betterName = goodName.replace("\'", '')
		bestName = betterName.replace('\"', '')
		defaultOutputFolder = bestName
		print("Updated Output folder is: %s" % defaultOutputFolder)
		self.defOutFolder = defaultOutputFolder

	def takePhotoOtherImage(self):
		newImagePath = str(input("enter path to test image: (must be exact!)"))
		self.log.info("user updated the test image path: %s" % (newImagePath))
		self.testImages[0] = newImagePath
		self.takePhotoNow()

	def exit(self):
		pass

