import cv2
import numpy as np
import math

"""
-------------------
Function findLens()
-------------------
Given an image containing a number of contours, this function
finds all the contours in the image.  It then uses approximations
of pi using perimeter and area to determine which contour is most
circular.  It then calculates the approximate radius and center
of that contour and returns them as a 'circle'.
INPUT:
 - img - unsigned 8-bit integer numpy array representing an image
 - scaling - compression ratio.  If not supplied, it will be set
    to 4
OUTPUT:
 - (x,y,r) - x,y are the centroid of the most circular contour, while
    r represents the average radius of that contour
"""

def findLens(img, scaling = None):
	# Input handling
	img = img.copy()
	if scaling == None:
		scaling = 4
	if len(img.shape) == 3:
		img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	
	# Resize the image and get new size
	height, width = img.shape
	img = cv2.resize(img, (width//scaling,height//scaling))
	height, width = img.shape
	
	# blur, threshold, and erode/dilate the image	
	img = cv2.medianBlur(img,9)
	ret, img = cv2.threshold(img,64,255,cv2.THRESH_BINARY)
	kernel = np.ones((9,9),np.uint8)
	img = cv2.erode(img,kernel,iterations=1)
	img = cv2.dilate(img,kernel,iterations=1)
	
	# Find the contours
	im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	# Determine which contour is most circular by finding which contour's
	#   perimeter and area most closely approximate pi
	circle = None
	circlePiError = 100
	for c in contours:
		cPi = (cv2.arcLength(c,True)**2) / (4*cv2.contourArea(c))
		cPiError = (cPi-math.pi)**2
		if cPiError < circlePiError:
			circle = c
			circlePiError = cPiError

	# Find the center and radius of the most circular contour
	M = cv2.moments(circle)
	x = M['m10']/M['m00']
	y = M['m01']/M['m00']
	r = math.sqrt(cv2.contourArea(circle)/math.pi)
	
	# unscale the circle parameters and round to integers
	(x,y,r) = (scaling*x,scaling*y,scaling*r)
	(x,y,r) = np.uint16(np.around((x,y,r)))
	return (x,y,r)

"""
if __name__ == '__main__':
	image = cv2.imread('withLens_DSC_0284.JPG')
	circle = findLens(image)
	print(circle)
	image = cv2.circle(image,(circle[0],circle[1]),circle[2],(0,0,255),3)
	cv2.imshow('circles',image)
	cv2.imwrite('foundCircle.png',image)
	cv2.waitKey(0)
"""