import tkinter as tk 
import logging
import os
import subprocess
import sys
import time
import pathlib

import gphoto2 as gp
import segmenter
import correlate
from linearActuator import LinearActuator
from cameraHandling import Camera
from displayHandling import FullScreenApp


class TestHandler():
	def __init__(self, testImages = None, defOutFolder = None, logLevelDefault = None):
		self.log = logging.getLogger("mainApp")
		#handler = logging.StreamHandler()
		# if logLevelDefault is None:
		# 	handler.setLevel(logging.INFO)
		# else:
		# 	handler.setLevel(logLevelDefault)
		# format = logging.Formatter('%(levelname)s -- %(message)s')
		# handler.setFormatter(format)
		# self.log.addHandler(handler)
		self.log.info("Initializing Test Handler...")

		#Set Default variables:
		if testImages is None:
			self.testImages = ['test.png']
		else:
			self.testImages = testImages

		if defOutFolder is None:
			self.defOutFolder = input("Enter Local Output Directory \n (new directories are automatically created): ")
			#self.defOutFolder = "RAW/"

		else:
			self.defOutFolder = defOutFolder

		#Initialize Singleton Variables and store a memory pointer in this object.
		self.camera = Camera.getInstance()
		self.actuator = LinearActuator.getInstance() #This should already have been initialized, but it will re-initialize if it hasn't been.
		self.display = FullScreenApp.getInstance()

	def printMainMenu(self):
		print("Current Output folder is: %s" % self.defOutFolder)
		print("Current test image is: %s" % self.testImages)
		print("Please Select from the following options:\n")
		self.myOpts = {
			1:self.takePhotoNow,
			2:self.changeOutputFolder,
			3:self.updateDisplayWithOtherImage,
			4:self.moveLensHolderOutOfWay,
			5:self.moveLensHolderIntoPath,
			6:self.oneClickTest,
			7:self.selectOutputFileFormat,
			8:self.exit			# Leave exit as last index
		}
		for key, opt in self.myOpts.items():
			print("\t%d. %s" % (key, opt.__name__))



	#@rename("Take Photo With First Test Image")
	def takePhotoNow(self):
		self.log.info("user is storing image in: %s with test photo: %s" % (self.defOutFolder, self.testImages))
		self.display.updateImage(self.testImages[0])
		target = self.camera.takePhoto(folderName = self.defOutFolder)
		self.log.info("photo saved at: %s" % target)

	def _takePhotoNowReturnsName(self, filePrefix = None, sampleFolder = None):
		
		if sampleFolder is not None:
			currentOutFolder = self.defOutFolder + "/" + sampleFolder
			self._makeFolder(currentOutFolder)
		else:
			currentOutFolder = self.defOutFolder
		self.log.info("user is storing image in: %s with test photo: %s" % (currentOutFolder, self.testImages))
		self.display.updateImage(self.testImages[0])
		target = self.camera.takePhoto(folderName = currentOutFolder, prefix = filePrefix)
		self.log.info("photo saved at: %s" % target)
		return target

	def changeOutputFolder(self):
		newFolderNameRaw = input("Enter new folder name: ")
		defaultOutputFolder = self._cleanInputs(newFolderNameRaw)
		self.log.info("Updated Output folder is: %s" % defaultOutputFolder)
		self.defOutFolder = defaultOutputFolder

	def _cleanInputs(self, usr_input):
		strippedName = usr_input.strip()
		nameWithSlashes = strippedName.replace(' ', '')
		goodName = nameWithSlashes.replace('\\', '')
		betterName = goodName.replace("\'", '')
		bestName = betterName.replace('\"', '')
		return bestName

	def updateDisplayWithOtherImage(self):
		newImagePath = str(input("enter path to test image: (must be exact!)"))
		self.log.info("user updated the test image path: %s" % (newImagePath))
		self.testImages[0] = newImagePath
		self.display.updateImage(self.testImages[0])

	def moveLensHolderOutOfWay(self):
		self.log.info("moving linear actuator out of the way...")
		self.actuator.moveOutOfPath()

	def moveLensHolderIntoPath(self):
		self.log.info("moving linear actuator into path...")
		self.actuator.moveIntoPath()

	def _makeFolder(self, dir_path):
		pathlib.Path(dir_path).mkdir(parents=True,exist_ok=True)

	def selectOutputFileFormat(self):
		outputFileFormatRaw = input("Which format, JPEG or NEF?: ")
		cleanedFormat = self._cleanInputs(outputFileFormatRaw)
		cleanedFormat = cleanedFormat.lower()
		if cleanedFormat[0] == 'j':
			self.camera.adjustMainSettings('imagequality', 'JPEG Fine')
			self.log.info('Camera Will save output as JPEG')
		elif cleanedFormat[0] == 'n':
			self.camera.adjustMainSettings('imagequality', 'NEF (Raw)')
			self.camera.adjustMainSettings('imagesize', '6000x4000')
			self.log.info('Camera Will save output as NEF')

	def oneClickTest(self):
		sampleFolderNameRaw = input("Enter Sample Name:")
		#self._makeFolder(self.defOutFolder + "/" + self._cleanInputs(sampleFolderNameRaw))
		self.display.updateImage(self.testImages[0])
		self.moveLensHolderOutOfWay()
		noLens = self._takePhotoNowReturnsName(filePrefix = "noLens_", sampleFolder = self._cleanInputs(sampleFolderNameRaw))
		self.moveLensHolderIntoPath()
		withLens = self._takePhotoNowReturnsName(filePrefix = "withLens_", sampleFolder = self._cleanInputs(sampleFolderNameRaw))
		# undev = segmenter.extractObjectsPngJpg(noLens)
		# print('undev segmented')
		# dev = segmenter.extractObjectsPngJpg(withLens)
		# print('dev segmented')
		# correlate.main(undev,dev,noLens[:-4])
		# print("Yeah this code is totally working!")
		
	def exit(self):
		pass

