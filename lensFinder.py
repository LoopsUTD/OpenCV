import cv2
import numpy as np
import math

def findLens(filename, scaling = None):
	if scaling == None:
		scaling = 4
	img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY)
	height, width = img.shape	
	img = cv2.resize(img, (width//scaling,height//scaling))
	height, width = img.shape	
	img = cv2.medianBlur(img,9)
	ret, img = cv2.threshold(img,64,255,cv2.THRESH_BINARY)
	kernel = np.ones((9,9),np.uint8)
	img = cv2.erode(img,kernel,iterations=1)
	img = cv2.dilate(img,kernel,iterations=1)
	im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	circle = None
	circlePiError = 100
	for c in contours:
		cPi = (cv2.arcLength(c,True)**2) / (4*cv2.contourArea(c))
		cPiError = (cPi-math.pi)**2
		if cPiError < circlePiError:
			circle = c
			circlePiError = cPiError
	M = cv2.moments(circle)
	x = M['m10']/M['m00']
	y = M['m01']/M['m00']
	r = math.sqrt(cv2.contourArea(circle)/math.pi)
	(x,y,r) = (scaling*x,scaling*y,scaling*r)
	(x,y,r) = np.uint16(np.around((x,y,r)))
	cv2.destroyAllWindows()
	return (x,y,r)

if __name__ == '__main__':
	circle = findLens('withLens_DSC_0284.JPG')
	print(circle)
	image = cv2.imread('withLens_DSC_0284.JPG')
	image = cv2.circle(image,(circle[0],circle[1]),circle[2],(0,0,255),3)
	cv2.imshow('circles',image)
	cv2.imwrite('foundCircle.png',image)
	cv2.waitKey(0)