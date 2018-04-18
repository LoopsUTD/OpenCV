import cv2
import numpy as np
from _operator import xor

# A NOTE ON NOTATION:
# The way numpy numbers its arrays is
# right-handed, just like in math, but turned
# 90 degrees clockwise.  That is, the pair
# (x,y) is:
#   ----- Y
#  |            RIGHT IN NUMPY
#  |
#  X
# Ordinarily, when programming, one expects the following,
# left-handed coordinate system, where (i,j) is:
#   ----- I
#  |            WRONG IN NUMPY
#  |
#  J

# - - - - - - - - - - - #
# Function filledCircle
# - - - - - - - - - - - #
#   Draws a filled circle 
#   in an image at a specified 
#   location
# Input:
#   x - x position of center
#   y - y position of center
#   r - radius of circle
#   img - 8-bit integer matrix
# Output:
#   modified version of img,
#   with circle drawn.
# NOTE:
#   matrices, like img, are
#   passed to functions by
#   reference, which means img
#   is automatically modified
#   in the calling function
# - - - - - - - - - - - #

def filledCircle(x,y,r,img):
	rsize = img.shape[0]
	csize = img.shape[1]
	maxDist = r*r
	for i in range(0,rsize):
		for j in range(0,csize):
			if (i-x)**2 + (j-y)**2 <= maxDist:
				img[i,j] = 255
	return img

# - - - - - - - - - - - #
# Function fourCorners
# - - - - - - - - - - - #
#   Draws a 2x2 checkerboard
#   in an image with center
#   at a specified location
# Input:
#   x - x position of center
#   y - y position of center
#   img - 8-bit integer matrix
# Output:
#   modified version of img,
#   with 2x2 grid drawn.
# NOTE:
#   matrices, like img, are
#   passed to functions by
#   reference, which means img
#   is automatically modified
#   in the calling function
# - - - - - - - - - - - #

def fourCorners(x,y,img):
	rsize = img.shape[0]
	csize = img.shape[1]
	for i in range(0,rsize):
		for j in range(0,csize):
			if i < x:
				if j > y:
					img[i,j] = 255
			else:
				if j < y:
					img[i,j] = 255
	return img

if __name__ == '__main__':
	image = np.zeros([900,1920,3])
	filledCircle(image.shape[0]//2,image.shape[1]//2,100,image[:,:,2])
	cv2.imshow('circleTest',image)
	cv2.waitKey(0)
	fourCorners(image.shape[0]//2,image.shape[1]//2,image[:,:,1])
	cv2.imshow('cornersTest',image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()