import cv2
import numpy as np

def findLens(filename):
	img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY)
	height, width = img.shape
	
	img = cv2.resize(img, (width//4,height//4))
	
	img = cv2.medianBlur(img,9)
	print('blur done')
	cv2.imshow('blur done',img)
	cv2.waitKey(0)
	ret, img = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
	print('thresh done')
	cv2.imshow('thresh done',img)
	cv2.waitKey(0)
	
#	cv2.imshow('edges',cv2.Canny(img,100,200))
#	cv2.waitKey(0)
	
	circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,img.shape[0]/16,param1=100,param2=30,minRadius=1800,maxRadius=2200)
	
	cv2.destroyAllWindows()
	
	return circles

if __name__ == '__main__':
	circles = findLens('DSC03070.JPG')
	print(circles)
	print(np.shape(circles))