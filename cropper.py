import numpy as np
import cv2			# only used when ran as main
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
	rsize = img.shape[0]	# These can be used to error-check the bounds of the copying iteration
	csize = img.shape[1]	# However, the lens should always fall entirely within the image, so it's *probably* irrelevant
	newImg = np.zeros(img.shape)
	newImg = cv2.circle(newImg,(x,y),r,(1,1,1),-1)
	newImg[:,:,0] = newImg[:,:,0] * img[:,:,0]
	newImg[:,:,1] = newImg[:,:,1] * img[:,:,1]
	newImg[:,:,2] = newImg[:,:,2] * img[:,:,2]
# 	maxDist = r**2
# 	for i in range(y-r,y+r):
# 		for j in range(x-r,x+r):
# 			if (i-circle[0])**2 + (j-circle[1])**2 >= maxDist:
# 				newImg[i,j] = img[i,j]
	return newImg

if __name__ == '__main__':
	image = cv2.imread('withLens_DSC_0284.JPG')
	print('image read')
	circle = lensFinder.findLens(image.copy())
	print('lens found')
	print(circle)
	image = cropToCircle(image,circle)
	cv2.imshow('cropped',image)
	cv2.waitKey(0)
	cv2.imwrite('cropped.png',image)
	cv2.destroyAllWindows()