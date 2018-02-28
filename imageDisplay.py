import numpy as np
import cv2

def display(imagename, x, y):
	cv2.namedWindow("output", cv2.WINDOW_NORMAL)        
	im = cv2.imread(imagename)													
	cv2.imshow("output", im) 
	height = im.shape[0]
	width = im.shape[1]
	print(im.shape)
	cv2.resizeWindow("output", (1920, 1080))
	cv2.moveWindow("output", x,y)
	cv2.waitKey(0)

if __name__ == '__main__':
	imagename = "dsc03113.jpg"
	x = 1920
	y = -5
	display(imagename,x,y)
	
	#1920, -5