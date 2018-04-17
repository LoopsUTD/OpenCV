import cv2
import numpy as np

def findLens(filename):
	img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY)
	height, width = img.shape
	
	img = cv2.resize(img, (width//4,height//4))
	
	img = cv2.medianBlur(img,3)
	print('blur done')
	cv2.imshow('blur done',img)
	cv2.waitKey(0)
	ret, img = cv2.threshold(img,64,255,cv2.THRESH_BINARY)
	print('thresh done')
	cv2.imshow('thresh done',img)
	cv2.waitKey(0)
	
	cv2.imshow('edges',cv2.Canny(img,100,200))
	cv2.waitKey(0)
	
	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
#	circles = np.uint16(np.around(circles))
	
	cv2.destroyAllWindows()
	
	return circles

if __name__ == '__main__':
	circles = findLens('withLens_DSC_0279.JPG')
	print(circles)
	print(np.shape(circles))