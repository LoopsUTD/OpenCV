import cv2
import matplotlib as m
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog

def main():
	plt.interactive(True)
	root = tk.Tk()
	root.withdraw()
	name=filedialog.askopenfilename()
	#name='lens3.txt'
	file=open(name,"r")
	map={}
	for line in file:
		linedat=line.split(",")
		map.update({(float(linedat[0]),float(linedat[1])):float((linedat[2][:-2]))})
	image=dictToImg(map,1.5)
	#cv2.imwrite("realData.png",image)
#	cv2.imshow('image',image)
	kernel = np.ones((5,5),np.uint8)
	dilated = cv2.dilate(image,kernel,iterations = 10)
	blurred=cv2.GaussianBlur(dilated,(55,55),0)
	plt.figure()
	plt.imshow(blurred,cmap='viridis')
	plt.colorbar()
	plt.savefig('{}c.png'.format(name))
	plt.show()

#	cv2.waitKey(0)	
	#dst,blurred=cv2.threshold(blurred,15,0,cv2.THRESH_TOZERO_INV)
	#colored=cv2.applyColorMap(blurred,cv2.COLORMAP_JET)
#	print(np.unique(image.reshape(-1,image.shape[2]),axis=0))
	cv2.imwrite('{}.png'.format(name[:-4]),blurred)
	#cv2.imwrite('{}c.png'.format(name[:-4]),colored)


"""def imscale(image):
	scaleimg=np.zeros(image.shape,float)
	scaleimg=255*(image/image.max())
	image=np.rint(scaleimg)
	return image
"""
def dictToImg(map,m=2):
	image=np.zeros((4016,6016,3),np.uint8)
	data=list(map.values())
	median=np.median(data)
	meddist=np.abs(data-np.median(data))
	mdev=np.median(meddist)
	for key,value in map.items():
		d=np.abs(value-median)
		if d/mdev < m:
			image[int(key[0]),int(key[1]),:]=value
		else:
			image[int(key[0]),int(key[1]),:]=0
	return image
def dictToFilledImg(map):
	image=np.zeros((4016,6016,3),np.uint8)
	for i in range(3000):
		for j in range (2000):
			mindist=50
			for key,value in map.items():
				distance=pow(pow(key[0]-i,2)+pow(key[1]-j,2),0.5)
				if distance<mindist:
					mindist=distance
					image[i,j]=value

def getImageDimensions()

if __name__=='__main__':
	main()

