import cv2
import numpy as np

def findLens(filename):
	img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY)
	img = cv2.medianBlur(img,5)
	print('blur done')
	
	circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=1900,maxRadius=2100)
	circles = np.uint16(np.around(circles))
	
	return circles

if __name__ == '__main__':
	circles = findLens('DSC03070.JPG')
	print(circles)
	print(np.shape(circles))