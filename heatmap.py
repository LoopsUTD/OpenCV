import cv2
import matplotlib as plot
import numpy as np
from blob import *

def main():
	name='DSC_0203.txt'
	map={}
	file=open(name,"r")
	for line in file:
		linedat=line.split(",")
		map.update({(float(linedat[0]),float(linedat[1])):float((linedat[2][:-2]))})
	#	image=imscale(image)
	image=dictToFilledImg(map)
	print(image.max())
#	cv2.imshow('image',image)
	kernel = np.ones((5,5),np.uint8)
	dilated = cv2.dilate(image,kernel,iterations = 5)
	blurred=cv2.medianBlur(dilated,55)
#	cv2.waitKey(0)	
	cv2.imwrite('heatmaptest.png',blurred)
	print(np.unique(image.reshape(-1,image.shape[2]),axis=0))

def imscale(image):
	scaleimg=np.zeros(image.shape,float)
	scaleimg=255*(image/image.max())
	image=np.rint(scaleimg)
	return image
def dictToImg(map):
	image=np.zeros((3000,2000,3),np.uint8)
	for key,value in map.items():
		image[int(key[0]),int(key[1]),:]=value

	return image
def dictToFilledImg(map):
	image=np.zeros((3000,2000,3),np.uint8)
	for i in range(3000):
		for j in range (2000):
			mindist=50
			for key,value in map.items():
				distance=pow(pow(key[0]-i,2)+pow(key[1]-j,2),0.5)
				if distance<mindist:
					mindist=distance
					image[i,j]=value
if __name__=='__main__':
	main()

