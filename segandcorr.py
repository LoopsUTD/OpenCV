import segmenter
import correlate
from time import *
import cv2
from multiprocessing import Pool,Process
import os

def analyze(name,imagefolder):
	start=time()
#	undevname="lens2_nolens_4pxG.png"
#	devname="lens2_wlens_4pxG.png"i
	undevname='{}{}{}'.format(imagefolder,name,"_nolens.JPG")
	devname='{}{}{}'.format(imagefolder,name,"_lens.JPG")
	print(undevname,devname)
	pool=Pool(2)
	asyncdev=pool.apply_async(seg,(devname,start))
	asyncundev=pool.apply_async(seg,(undevname,start))
	undev=asyncundev.get()
	dev=asyncdev.get()
	correlate.main(undev,dev,name)
	print ('Total time elapsed: {} seconds'.format(time()-start))
def seg(image,start):
	segmented=segmenter.extractObjectsPngJpg(image)
	print('{} segmented'.format(image))
	print(time()-start)
#	for blobs in undev:
#		print("u")
#		print(blobs)
	return segmented
if __name__=="__main__":	
	analyze('lens3',"../JPG_ADJUSTED_SIZE/")


