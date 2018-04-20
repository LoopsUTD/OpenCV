import segmenter
import correlate
import visualize
from time import *
import cv2
from multiprocessing import Pool,Process
import os
import tkinter as tk
from tkinter import filedialog
import lensFinder
import cropper
import rawpy

def analyze(undevpath,devpath,dirname,lensfind):
	start=time()
	print(undevpath,devpath)
	shortname=parseName(devpath)
	pool=Pool(2)
	asyncdev=pool.apply_async(seg,(devpath,start,lensfind))
	asyncundev=pool.apply_async(seg,(undevpath,start,lensfind))
	undev=asyncundev.get()
	dev=asyncdev.get()
	mapping=correlate.main(undev,dev,devpath[:-4])
	print ('Images correlated in {} seconds'.format(time()-start))
	visualize.execute(mapping,dirname,shortname)	
	print('Visualization generated in {} seconds'.format(time()-start))
def seg(path,start,lensfind):	
	circle=getCropCircle(lensfind)
	imgSplit = path.split('.')
	if imgSplit[len(imgSplit) - 1].lower() == 'nef':
		with rawpy.imread(path) as raw:
			image = raw.postprocess(output_bps=8)
		image=cropper.cropToCircle(image,circle)
		segmented=segmenter.extractObjectsNef(image) #Try the Raw files
	else:	
		image = cv2.imread(path)
		image = cropper.cropToCircle(image,circle)
		segmented=segmenter.extractObjectsPngJpg(image)
	
	print('{} segmented in {} seconds'.format(image,time()-start))
#	for blobs in undev:
#		print("u")
#		print(blobs)
	return segmented
def parseName(devpath):
	namearr=devpath.split('/')
	shortname=namearr[len(namearr)-1]
	shortname=shortname[:-4]	
	return shortname 
def getCropCircle(path):
	image=cv2.imread(path)
	circle=lensFinder.findLens(image)	
	return circle
if __name__=="__main__":	
	root=tk.Tk()
	root.withdraw()
	outdir=filedialog.askdirectory(title="Double click on desired output folder")
	undevpath = filedialog.askopenfilename(title="Select image without lens")
	devpath = filedialog.askopenfilename(title="Select image with lens")
	lensfind = filedialog.askopenfilename(title="Select lens finding")
	inarr=devpath.split('/')	
	analyze(undevpath,devpath,outdir, lensfind)
	


