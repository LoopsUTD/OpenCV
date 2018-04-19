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
	(x,y,r) = circle
	newImg = np.zeros(img.shape)
	newImg = cv2.circle(newImg,(x,y),r,(1,1,1),-1)
	newImg[:,:,0] = newImg[:,:,0] * img[:,:,0]
	newImg[:,:,1] = newImg[:,:,1] * img[:,:,1]
	newImg[:,:,2] = newImg[:,:,2] * img[:,:,2]
	return newImg

if __name__ == '__main__':
	image = cv2.imread('withLens_DSC_0284.JPG')
	circle = lensFinder.findLens(image.copy())
	image = cropToCircle(image,circle)
	cv2.imshow('cropped',image)
	cv2.waitKey(0)
	cv2.imwrite('cropped.png',image)
	cv2.destroyAllWindows()