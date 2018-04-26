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
import globalPower
import rawpy
import os


def analyze(undevpath,devpath,dirname,lensFindPath,lensname,unMagPath,magPath):
	start=time()
	pool=Pool(2)
	print(undevpath,devpath)
	lensFindImg=loadImage(lensFindPath)	
	print('Finding circular mask...')
	circle=lensFinder.findLens(lensFindImg)
	print ('Circular mask found in {} seconds.'.format(time()-start))
	print('Determining magnification factor...')
	unMag=loadImage(unMagPath)	
	mag=loadImage(magPath)
	unMag=cropper.cropToCircle(unMag,circle)
	mag=cropper.cropToCircle(mag,circle)
	magnification,power=globalPower.calculatePower(unMag,mag)
	print('Magnification({}) found in {} seconds.'.format(magnification, time()-start))
	print('Beginning parallel processing of images...')
	asyncdev=pool.apply_async(seg,(devpath,circle,start))
	asyncundev=pool.apply_async(seg,(undevpath,circle,start))
	undev=asyncundev.get()
	dev=asyncdev.get()
	print('Correcting for global power...')
	dev=globalPower.demagnify(dev,circle,magnification)
	print('Global power corrected in {} seconds.'.format(time()-start))
	print('Correlating images...')
	mapping=correlate.main(undev,dev,dirname,lensname)
	print ('Images correlated in {} seconds.'.format(time()-start))
	print('Creating data visualization...')
	visualize.execute(mapping,dirname,lensname,circle,start)	
	print('Visualization generated in {} seconds.'.format(time()-start))
def seg(path,circle,start):	
	image=loadImage(path)
	print('Cropping to lens area...')
	image=cropper.cropToCircle(image,circle)
	print('Image cropped in {} seconds.'.format(time()-start))
	print('Segmenting {}...'.format(path))
	#cv2.imwrite('{}_segmented.png'.format(path),image)
	segmented=segmenter.extractObjects(image) #Try the Raw files
	print('{} segmented in {} seconds.'.format(path,time()-start))
	return segmented

def loadImage(filename):
	imgSplit=filename.split('.')
	imgtype=imgSplit[len(imgSplit) - 1].lower() 
	if imgtype == 'nef':
		with rawpy.imread(filename) as raw:

			image = raw.postprocess(output_bps=8)
		image=cropper.cropToCircle(image,circle)
		segmented=segmenter.extractObjectsNef(image) #Try the Raw files
	else:	
		image = cv2.imread(filename)
	return image

def getCropCircle(path):
	imgSplit = path.split('.')
	if imgSplit[len(imgSplit) - 1].lower() == 'nef':
		with rawpy.imread(path) as raw:
			image = raw.postprocess(output_bps=8)

	else:
		image=cv2.imread(path)
	circle=lensFinder.findLens(image)	
	return circle
if __name__=="__main__":	
	root=tk.Tk()
	root.withdraw()
	indir=filedialog.askdirectory(title="Double click on folder containing test images")
	outdir=filedialog.askdirectory(title="Double click on desired output folder")
	files=os.listdir(indir)
	undevpath=[f for f in files if f.startswith('noLens')][0]
	undevpath='{}/{}'.format(indir,undevpath)
	devpath=[f for f in files if f.startswith('withLens')][0]
	devpath='{}/{}'.format(indir,devpath)
	unMagPath=[f for f in files if f.startswith('power_noLens')][0]
	unMagPath='{}/{}'.format(indir,unMagPath)
	magPath=[f for f in files if f.startswith('power_withLens')][0]
	magPath='{}/{}'.format(indir,magPath)
	inarray=indir.split('/')
	lensname=inarray[len(inarray)-1]
	lensfind=[f for f in files if f.startswith('lensFinding')][0]
	lensfind='{}/{}'.format(indir,lensfind)
	"""
	undevpath = filedialog.askopenfilename(title="Select image without lens")
	devpath = filedialog.askopenfilename(title="Select image with lens")
	lensfind = filedialog.askopenfilename(title="Select lens finding")
	"""
	analyze(undevpath,devpath,outdir,lensfind,lensname,unMagPath,magPath)
	


