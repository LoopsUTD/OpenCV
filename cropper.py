import numpy as np
import cv2

# Function cropImage()
#  Given an image and a desirable circle,
#  the function eliminates all image features
#  outside the circle.
# INPUTS:
#  img	- 2-D array (1 or 3 channel) bitmap of image
#  circle - 3-tuple, (x-center, y-center, radius)
# OUTPUTS:
#  newImg	- black image, with everything inside
#			region of interest copied over

def cropToCircle(img, circle):
	img = img.copy()
	if len(img.shape)==3:
		img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	(x,y,r) = circle
	newImg = np.zeros(img.shape, dtype=img.dtype)
	newImg = cv2.circle(newImg,(x,y),r,(1,1,1),-1)
	newImg[:,:] = newImg[:,:] * img[:,:]
#	newImg=newImg[(y-r):(y+r),(x-r):(x+r),:]
	return newImg