import cv2

def display(imagename, x, y):
	cv2.namedWindow("output", cv2.WINDOW_NORMAL)        
	im = cv2.imread(imagename)													
	cv2.imshow("output", im) 
	height = im.shape[0]
	width = im.shape[1]
	cv2.resizeWindow("output", (width, height))	#ensures the image will be displayed at precisely 100% scale
	cv2.moveWindow("output", x,y)				#places the corner of the display window at x,y - unfortunately meaning the image is offset
	cv2.waitKey(0)

if __name__ == '__main__':
	imagename = "dsc03113.jpg"
	x = 1920
	y = -5
	display(imagename,x,y)
	
	#1920, -5