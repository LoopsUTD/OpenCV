import cv2
import numpy as np

def findLens(filename, scaling = None):
	if scaling == None:
		scaling = 4

	img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY)
	height, width = img.shape	
	img = cv2.resize(img, (width//scaling,height//scaling))
	height, width = img.shape	
	
	img = cv2.medianBlur(img,9)
	print('blur done')
	cv2.imshow('blur done',img)
	cv2.waitKey(0)
	ret, img = cv2.threshold(img,64,255,cv2.THRESH_BINARY)
	print('thresh done')
	cv2.imshow('thresh done',img)
	cv2.waitKey(0)
	kernel = np.ones((9,9),np.uint8)
	img = cv2.erode(img,kernel,iterations=1)
	img = cv2.dilate(img,kernel,iterations=1)
	print('close done')
	cv2.imshow('close done',img)
	cv2.waitKey(0)	
	cv2.imshow('edges',cv2.Canny(img,100,200))
	cv2.waitKey(0)

#	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100)	
	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,30,param1=30,param2=15,minRadius=0,maxRadius=height//2)
	if circles.dtype != None:
		circles = np.uint16(np.around(circles))	
		circles = circles * scaling
	
	cv2.destroyAllWindows()
	
	return circles

if __name__ == '__main__':
	circles = findLens('withLens_DSC_0284.JPG')
	print(circles)
	print(np.shape(circles))
	image = cv2.imread('withLens_DSC_0284.JPG')
#	image = np.zeros(image.shape)
	for i in circles[0,:]:
		cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
	cv2.imshow('circles',image)
	cv2.imwrite('foundCircle.png',image)
	cv2.waitKey(0)