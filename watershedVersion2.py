def main():
	import cv2
	import numpy as np 
	from matplotlib import pyplot as plt

	name = "croppedNoLens.jpg"
	img = cv2.imread(name)
		
	shifted = cv2.pyrMeanShiftFiltering(img, 21, 51)

	gray_img = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
	
	#dist_transform = cv2.distanceTransform(gray_img,cv2.DIST_L2,5)
#ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
	ret, thresh = cv2.threshold(gray_img, 70, 255, cv2.THRESH_BINARY)

	#Website for Thresholding: https://www.learnopencv.com/opencv-threshold-python-cpp/

	#Website for this code: https://www.pyimagesearch.com/2015/11/02/watershed-opencv/
	# ##Do kernel convolution noise reduction
	# # noise removal
	kernel = np.ones((8,8),np.uint8)
	opening = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel, iterations = 3)
	# #sure_bg = cv2.dilate(opening,kernel,iterations=2)
	dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
	ret2, thresh50 = cv2.threshold(dist,0.5*dist.max(),255,0)
	ret2, thresh25 = cv2.threshold(dist,0.25*dist.max(),255,0)
	ret2, thresh75 = cv2.threshold(dist,0.75*dist.max(),255,0)
	
	threshTest = np.uint8(thresh25)
	ret3, markers = cv2.connectedComponents(threshTest)
	#markers = markers + 1
	markers = cv2.watershed(img,markers)
	#markers = markers + 1
	img[markers == -1] = [255,0,0]
	print(markers)
	#img[markers == -1] = [255,0,0]
	# #Lets find contours in the thresholded images
	# cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	# print("[INFO] {} unique contours found".format(len(cnts)))

	# for (i,c) in enumerate(cnts):
	# 	#Draw the contours
	# 	((x,y), _) = cv2.minEnclosingCircle(c)
	# 	#cv2.putText(opening, "#[]".format(i + 1), (int(x) - 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
	# 	cv2.drawContours(opening, [c], -1, (128,128,128), -2)

	# #cv2.imshow("Image", opening)
	# #cv2.waitKey(0)
	#plt.subplot(211),plt.imshow(dist)
	#plt.title('DistanceTransform'), plt.xticks([]), plt.yticks([])
	#plt.subplot(222),plt.imshow(thresh25)
	#plt.title('25% Threshold'), plt.xticks([]), plt.yticks([])
	#plt.subplot(223),plt.imshow(markers)
	#plt.title('markers'), plt.xticks([]), plt.yticks([])
	plt.imshow(img)
	plt.title('img')#, plt.xticks([]), plt.yticks([])
	# plt.imshow(dist, 'gray')
	# plt.show()
	# plt.imshow(thresh2, 'gray')
	plt.show()


if __name__ == "__main__":
	main()