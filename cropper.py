import numpy as np
import cv2
import lensFinder	# only used when ran as main

# Function cropImage()
#  Given an image and a desirable circle,
#  the function eliminates all image features
#  outside the circle.
# INPUTS:
#  img	- 2-D array (3 channel) bitmap of image
#  circle - 3-tuple, (x-center, y-center, radius)
# OUTPUTS:
#  newImg	- black image, with everything inside
#			region of interest copied over

def cropToCircle(img, circle):
	if len(img.shape)==3:
		img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	(x,y,r) = circle
	newImg = np.zeros(img.shape, dtype=img.dtype)
	newImg = cv2.circle(newImg,(x,y),r,(1,1,1),-1)
	newImg[:,:] = newImg[:,:] * img[:,:]
#	newImg=newImg[(y-r):(y+r),(x-r):(x+r),:]
	return newImg

if __name__ == '__main__':
	image = cv2.imread('withLens_DSC_0284.JPG')
	circle = lensFinder.findLens(image.copy())
	image = cv2.imread('DSC_0286.JPG')
	image = cropToCircle(image,circle)
	cv2.imshow('cropped',image)
	cv2.waitKey(0)
	cv2.imwrite('cropped.png',image)
	circle2 = lensFinder.findLens(image)
	print(circle)
	print(circle2)
	cv2.destroyAllWindows()
