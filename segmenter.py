import cv2
import numpy
from blob import Blob

# WARNING: UNEXPECTED BEHAVIOR MAY OCCUR #
"""
The final function called by extractObjects, segmentInfo(),
utilizes (~^.^)~ RECURSION ~(^.^~).  When it finds an
above-threshold pixel, segmentInfo() calls fill().  fill()
recursively calls itself to explore entire blobs.  Python
has a built-in maximum recursion depth of 1000.  Currently,
this limit is unchanged by the program.  So, if a segment
of more than 1000 pixels is found, is possible for the
program to crash.  However, our photos of screen pixels
*shouldn't* contain segments over 1000 pixels.
"""

# INPUT:  name of .png photograph file
# OUTPUT: array of found blob objects
# FILE I/O: loads image from file of given name


def extractObjects(img,thresh=None):
	image = greenscale(img)
	if thresh == None:
		thresh = 128
	image = threshold(image,thresh)
	image = segment(image)
	foundBlobs = segmentInfo(image)
	return foundBlobs


def loudExtractObjects(image,thresh=None):
	cv2.imshow("greenscale",image)
	cv2.waitKey(0)
	image = greenscale(image)
	cv2.imshow("greenscale",image)
	cv2.waitKey(0)
	if thresh == None:
		thresh = 128
	image = threshold(image,thresh)
	cv2.imshow("greenscale",image)
	cv2.waitKey(0)
	image = segment(image)
	cv2.imshow("greenscale",image.astype(dtype='uint8'))
	cv2.waitKey(0)
	foundBlobs = segmentInfo(image)
	return foundBlobs

# Sub-functions

# GREENSCALE()
# INPUT:  array representation of image, 1- or 3-channel
# OUTPUT: 1-channel representation of image
# This is a wrapper function that checks whether grayscale needs to be run or not
#   Its name originates from when the only color of interest in the images was green

def greenscale(image):
	if len(image.shape) == 3:
		image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	return image

# THRESHOLD()
# INPUT:  1-channel array representing an image
# OUTPUT: Array containing only 0 (low values) or 255 (high values) in each entry

def threshold(image,thresh):
	for a in numpy.nditer(image, op_flags=['readwrite']):
		if a >= thresh:
			a[...] = 255
		else:
			a[...] = 0
	return image

# FILL()
# INPUT:  Pixel location of part of blob\
# TASK:   Recursively "Fills" a blob from one found pixel
# OUTPUT: None per se, but it checks all neighbors

def fill(image,i,j,h,w,index):
	image[i,j] = index
	if i > 0 and image[i-1,j] == 255:
		fill(image,i-1,j,h,w,index)
	if i+1 < h and image[i+1,j] == 255:
		fill(image,i+1,j,h,w,index)
	if j > 0 and image[i,j-1] == 255:
		fill(image,i,j-1,h,w,index)
	if j+1 < w and image[i,j+1] == 255:
		fill(image,i,j+1,h,w,index)
	return

# SEGMENT()
# INPUT:  Thresholded image
# OUTPUT: Image with isolated segments

def segment(image):
	index = 256	 # Starts at 256 because the largest number in the image will be 255
	h = len(image)
	w = len(image[1])
	image = image.astype(dtype='uint16')
	
	for i in range(h//4):
		for j in range(w//4):
			if image[4*i,4*j] > 0 and image[4*i,4*j] < 256:	 # if the pixel is part of an object and not yet marked
				fill(image,4*i,4*j,h,w,index)
				index = index + 1

	return image

# SEGMENTINFO()
# INPUT:  Image with isolated and labeled segments
# OUTPUT: Array of blob objects

def segmentInfo(img):
	h = len(img)
	w = len(img[1])
	b = {}
	
	for i in range(h):
		for j in range(w):
			if img[i,j] != 0:
				if img[i,j] not in b:
					b[img[i,j]] = [1,i,j]
				else:
					b[img[i,j]] = [b[img[i,j]][0]+1,b[img[i,j]][1]+i,b[img[i,j]][2]+j]
	blobs = list()
	for key in b:
		ssn = key
		x   = b[key][1] // b[key][0]
		y   = b[key][2] // b[key][0]
		newBlob = Blob(ssn,x,y)
		blobs.append(newBlob)
	return numpy.asarray(blobs)