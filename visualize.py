import cv2
import matplotlib as m
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
from time import *
import cropper

pixPerMM = 58
maxDev=0.1

def execute(map,dirname,shortname,circle,start):
	print('Creating sparse heatmap...')
	image=dictToImg(map,10)
	print('Deviation map generated in {} seconds.'.format(time()-start))
	spotsize=1*pixPerMM
	even=spotsize
	if(even%2==0):
		spotsize=int(spotsize+1)
	fill=11
	print('Downsampling to correct resolution...')
	image=downsample(image,int(fill),int(spotsize))
	print('Downsampled in {} seconds.'.format(time()-start))
	createVisualization(image,dirname,shortname,circle,start)

def downsample(image,fill,spotsize):
	kernel = np.ones((5,5),np.uint8)
	dilated = cv2.dilate(image,kernel,iterations = fill)
	blurred=cv2.medianBlur(dilated, spotsize)
	return blurred

def createVisualization(image,dirname,shortname,circle,start):
	print('Creating heatmap...')
	name='{}/{}'.format(dirname,shortname)
	image=image/(pixPerMM)	
	#plt.interactive(True)
	plt.figure()
	plt.imshow(image,cmap='viridis')
	cbar=plt.colorbar()
	cbar.ax.get_yaxis().labelpad = 15
	cbar.ax.set_ylabel('Spatial Deviation (mm)', rotation=270)
	plt.clim(0,maxDev) 
	plt.title('Deviation Map for {}'.format(shortname))
	plt.xlabel('Horizontal Pixel Position')
	plt.ylabel('Vertical Pixel Position')
	plt.savefig('{}_heatmap.png'.format(name),bbox_inches='tight',dpi=1200)
	cv2.imwrite('After heatmap.png',image)
	print('Heatmap created in {} seconds.'.format(time()-start))
	print('Creating histogram...')
	plt.figure()
	cropped=selectCircle(image,circle)
	plt.hist(cropped)
	plt.draw()
	plt.title('Deviation Histogram for {}'.format(shortname))
	plt.xlabel('Deviation Intensity (mm moved)')
	plt.ylabel('Area of Lens (3350 Pixels = 1 $mm^2$)')
	plt.savefig('{}_histogram.png'.format(name),bbox_inches='tight',dpi=1200)
	print('Histogram created in {} seconds.'.format(time()-start))
	
def selectCircle(image,circle):
	(x,y,r)=circle
	onedim=[]
	h = len(image)
	w = len(image[1])
	for i in range(y-r,y+r):
		for j in range(x-r,x+r):
			dist=pow(pow(j-x,2)+pow(i-y,2),0.5)
			if dist < r:
				onedim.append(image[i,j])
	#cropped=cropper.cropToCircle(image,circle)
	#cv2.imwrite('croppedheatmap.png',cropped)
	#onedim=np.reshape(cropped,-1)
	
	return np.asarray(onedim)

def imscale(image):
	scaleimg=np.zeros(image.shape,float)
	scaleimg=255*(image/image.max())
	image=np.rint(scaleimg)
	return image

def dictToImg(map,m=10):
	image=np.zeros((4016,6016),np.uint8)
	data=list(map.values())
	median=np.median(data)
	meddist=np.abs(data-np.median(data))
	mdev=np.median(meddist)
	for key,value in map.items():
		d=np.abs(value-median)
		if d/mdev < m:
			image[int(key[0]),int(key[1])]=value
		else:
			image[int(key[0]),int(key[1])]=0
	return image

def readFromFile(name):
	file=open(name,"r")
	map={}
	for line in file:
		linedat=line.split(",")
		map.update({(float(linedat[0]),float(linedat[1])):float((linedat[2][:-2]))})
	return map,name

if __name__=='__main__':
	root = tk.Tk()
	root.withdraw()
	name=filedialog.askopenfilename(title="Choose text data to visualize")
	map,name=readFromFile(name)
	nmarray=name.split('/')
	shortname=nmarray[len(nmarray)-2]
	dirname=""
	for i in range(len(nmarray)-1):
		dirname+=nmarray[i]+"/"
	print(shortname)	
	execute(map,dirname,shortname,circle=None)

