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
	undevname=undevpath
	devname=devpath
	print(undevname,devname)
	pool=Pool(2)
	asyncdev=pool.apply_async(seg,(devname,start))
	asyncundev=pool.apply_async(seg,(undevname,start))
	undev=asyncundev.get()
	dev=asyncdev.get()
	mapping=correlate.main(undev,dev,devpath[:-4])
	print ('Images correlated in {} seconds'.format(time()-start))
	visualize.execute(mapping,devname)	
	print('Visualization generated in {} seconds'.format(time()-start))
def seg(image,start):
	imgSplit = image.split('.')
	if imgSplit[len(imgSplit) - 1].lower() == 'nef':
		segmented=segmenter.extractObjectsNef(image) #Try the Raw files
	else:
		segmented=segmenter.extractObjectsPngJpg(image)
	
	print('{} segmented in {} seconds'.format(image,time()-start))
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
	


