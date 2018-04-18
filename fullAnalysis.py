import segmenter
import correlate
import visualize
from time import *
import cv2
from multiprocessing import Pool,Process
import os
import tkinter as tk
from tkinter import filedialog

def analyze(undevpath,devpath):
	start=time()
#	undevname="lens2_nolens_4pxG.png"
#	devname="lens2_wlens_4pxG.png"i
#	undevname='{}{}{}'.format(imagefolder,name,"_nolens.JPG")
#	devname='{}{}{}'.format(imagefolder,name,"_lens.JPG")
	undevname=undevpath
	devname=devpath
	print(undevname,devname)
	pool=Pool(2)
	asyncdev=pool.apply_async(seg,(devname,start))
	asyncundev=pool.apply_async(seg,(undevname,start))
	undev=asyncundev.get()
	dev=asyncdev.get()
	correlate.main(undev,dev,undevpath[:-4])
	print ('Total time elapsed: {} seconds'.format(time()-start))
def seg(image,start):
	imgSplit = image.split('.')
	if imgSplit[len(imgSplit) - 1].lower() == 'nef':
		segmented=segmenter.extractObjectsNef(image) #Try the Raw files
	else:
		segmented=segmenter.extractObjectsPngJpg(image)
	
	print('{} segmented'.format(image))
	print(time()-start)
#	for blobs in undev:
#		print("u")
#		print(blobs)
	return segmented
if __name__=="__main__":	
	root=tk.Tk()
	root.withdraw()
	undevpath = filedialog.askopenfilename()
	devpath = filedialog.askopenfilename()
	analyze(undevpath,devpath)
	


