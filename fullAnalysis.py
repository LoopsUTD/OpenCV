"""
This script runs all of the relevant analysis code. 
Given an input folder containing 5 files:
noLens*
withLens*
power_noLens*
power_withLens*
lensFinding*

This will write a .txt file containing the raw data,
a histogram, and a heatmap to the folder indicated as the output folder.
"""

import segmenter
import correlate
import visualize
from time import *
import cv2
from multiprocessing import Pool,Process
import os
import tkinter as tk
from tkinter import filedialog
import shapeFinder
import cropper
import globalPower
import rawpy

def analyze(lensname,dirname,lensFindPath,unMagPath,magPath,undevPath,devPath):
	start = time()
	pool  = Pool(2)
	print(undevPath,devPath)

	lensFindImg = loadImage(lensFindPath)	
	circle = shapeFinder.findCircle(lensFindImg)
	print('Determining magnification factor...')

	unMag = loadImage(unMagPath)	
	mag   = loadImage(magPath)
	unMag = cropper.cropToCircle(unMag,circle)
	mag   = cropper.cropToCircle(mag,circle)
	magnification, power = globalPower.calculatePower(unMag,mag)	# returns magnification ratio and dioptic power (dioptic power currently unused)
	print('Magnification({}) found in {} seconds.'.format(magnification, time()-start))

	print('Beginning parallel processing of images...')
	asyncdev=pool.apply_async(seg,(devPath,circle,start))
	asyncundev=pool.apply_async(seg,(undevPath,circle,start))
	undev=asyncundev.get()
	dev=asyncdev.get()

	print('Correcting for global power...')
	dev = globalPower.demagnify(dev,circle,magnification)
	print('Global power corrected in {} seconds.'.format(time()-start))

	print('Correlating images...')
	mapping = correlate.main(undev,dev,dirname,lensname)
	print('Images correlated in {} seconds.'.format(time()-start))

	print('Creating data visualization...')
	visualize.execute(mapping,dirname,lensname,circle,start)	
	print('Visualization generated in {} seconds.'.format(time()-start))

def seg(path,circle,start):	
	image = loadImage(path)
	image = cropper.cropToCircle(image,circle)
	print('Segmenting {}...'.format(path))
	segmented = segmenter.extractObjects(image)
	print('{} segmented in {} seconds.'.format(path,time()-start))
	return segmented

def loadImage(filename):
	imgSplit = filename.split('.')
	imgtype  = imgSplit[len(imgSplit) - 1].lower() 
	if imgtype == 'nef':
		with rawpy.imread(filename) as raw:
			image = raw.postprocess(output_bps=8)
	else:	
		image = cv2.imread(filename)
	return image

if __name__=="__main__":
	# Initialize UI Framework for file selection
	root = tk.Tk()
	root.withdraw()
	
	# Ask the user for input and output directories
	indir  = filedialog.askdirectory(title="Double click on folder containing test images")
	outdir = filedialog.askdirectory(title="Double click on desired output folder")
	
	# Determine lens name using directory name
	inarray = indir.split('/')
	lensname = inarray[len(inarray)-1]

	# Locate the file names of each of the five images used in analysis
	files  = os.listdir(indir)
	lensFindPath = [f for f in files if f.startswith('lensFinding')][0]
	unMagPath    = [f for f in files if f.startswith('power_noLens')][0]
	magPath      = [f for f in files if f.startswith('power_withLens')][0]
	undevpath    = [f for f in files if f.startswith('noLens')][0]
	devpath      = [f for f in files if f.startswith('withLens')][0]
	
	# Append the input directory name to the image names
	lensFindPath = '{}/{}'.format(indir,lensFindPath)
	unMagPath    = '{}/{}'.format(indir,unMagPath)
	magPath      = '{}/{}'.format(indir,magPath)
	undevpath    = '{}/{}'.format(indir,undevpath)
	devpath      = '{}/{}'.format(indir,devpath)

	# Run analysis code
	analyze(lensname,outdir,lensFindPath,unMagPath,magPath,undevpath,devpath)