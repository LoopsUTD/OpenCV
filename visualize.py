import cv2
import matplotlib as m
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog

def execute(map,dirname,shortname):
	image=dictToImg(map,10)
	image=downsample(image,fill=11,spotsize=55)
	createVisualization(image,dirname,shortname)
	#image=imscale(image)
	#cv2.imwrite("realData.png",image)
#	cv2.imshow('image',image)
def downsample(image,fill,spotsize):
	kernel = np.ones((5,5),np.uint8)
	dilated = cv2.dilate(image,kernel,iterations = fill)
#	cv2.imwrite('{}_dilated.png'.format(name[:-4]),dilated)
	blurred=cv2.medianBlur(dilated, spotsize)
#	cv2.imwrite('{}_blurred.png'.format(name[:-4]),blurred)	
#j	colored=cv2.applyColorMap(blurred,cv2.COLORMAP_JET)
#jjjj	cv2.imwrite('{}_colored.png'.format(name[:-4]),colored)
	return blurred
def createVisualization(image,dirname,shortname):
	name='{}/{}'.format(dirname,shortname)
	plt.interactive(True)
	plt.figure()
	plt.imshow(image,cmap='viridis')
	plt.colorbar()
	plt.clim(0,10)
	plt.title('Deviation Map for {}'.format(shortname[:-4]))
	plt.xlabel('Horizontal pixel position')
	plt.ylabel('Vertical pixel position')
	plt.savefig('{}_heatmap.png'.format(name[:-4]))
	plt.figure()
	plt.hist(np.reshape(image,-1))
	plt.draw()
	plt.title('Deviation Histogram for {}'.format(shortname[:-4]))
	plt.xlabel('Deviation intensity (Pixels moved)')
	plt.ylabel('Number of Blobs')
	plt.savefig('{}_histogram.png'.format(name[:-4]))
#	cv2.waitKey(0)	
	#dst,blurred=cv2.threshold(blurred,15,0,cv2.THRESH_TOZERO_INV)
#	print(np.unique(image.reshape(-1,image.shape[2]),axis=0))
	#cv2.imwrite('{}.png'.format(name[:-4]),image)

def imscale(image):
	scaleimg=np.zeros(image.shape,float)
	scaleimg=255*(image/image.max())
	image=np.rint(scaleimg)
	return image

def dictToImg(map,m=10):
	image=np.zeros((4016,6016,1),np.uint8)
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


if __name__=='__main__':
	root = tk.Tk()
	root.withdraw()
	name=filedialog.askopenfilename(title="Choose text data to visualize")
	#name='lens3.txt'
	file=open(name,"r")
	map={}
	for line in file:
		linedat=line.split(",")
		map.update({(float(linedat[0]),float(linedat[1])):float((linedat[2][:-2]))})

	execute(map,name)

