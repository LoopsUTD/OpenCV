def main():
	import cv2
	import numpy as np 
	from matplotlib import pyplot as plt

	name = "croppedNoLens.jpg"
	img = cv2.imread(name)
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	##Do kernel convolution noise reduction
	# noise removal
	kernel = np.ones((5,5),np.uint8)
	opening = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel, iterations = 3)
	#sure_bg = cv2.dilate(opening,kernel,iterations=2)
	
	#Lets find contours in the thresholded images
	cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	print("[INFO] {} unique contours found".format(len(cnts)))

	for (i,c) in enumerate(cnts):
		#Draw the contours
		((x,y), _) = cv2.minEnclosingCircle(c)
		#cv2.putText(opening, "#[]".format(i + 1), (int(x) - 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
		cv2.drawContours(opening, [c], -1, (128,128,128), -2)

	#cv2.imshow("Image", opening)
	#cv2.waitKey(0)

	plt.imshow(opening, 'gray')
	plt.show()



if __name__ == "__main__":
	main()