import cv2
import matplotlib as m
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog


pixPerMM = 58
maxDev=0.1
def execute(map,dirname,shortname,circle):
	image=dictToImg(map,10)
	spotsize=5*pixPerMM
	even=spotsize
	if(even%2==0):
		spotsize=int(spotsize+1)
	fill=11
	image=downsample(image,int(fill),int(spotsize))
	createVisualization(image,dirname,shortname,circle)
def downsample(image,fill,spotsize):
	kernel = np.ones((5,5),np.uint8)
	dilated = cv2.dilate(image,kernel,iterations = fill)
	blurred=cv2.medianBlur(dilated, spotsize)
	return blurred
def createVisualization(image,dirname,shortname,circle):
	name='{}/{}'.format(dirname,shortname)
	#plt.interactive(True)
	plt.figure()
	image=image/(pixPerMM)	
	plt.imshow(image,cmap='viridis')
	plt.colorbar()
	plt.clim(0,maxDev)
	plt.title('Deviation Map for {}'.format(shortname))
	plt.xlabel('Horizontal pixel position')
	plt.ylabel('Vertical pixel position')
	plt.savefig('{}_heatmap.png'.format(name),dpi=1200)
	plt.figure()
	cropped=selectCircle(image,circle)
	plt.hist(np.reshape(cropped,-1))
	plt.draw()
	plt.title('Deviation Histogram for {}'.format(shortname))
	plt.xlabel('Deviation intensity (mm moved)')
	plt.ylabel('Area of lens (3350 pixels = 1 square mm)')
	plt.savefig('{}_histogram.png'.format(name),dpi=1200)
def selectCircle(image,circle):
	onedim=[]
	h = len(image)
	w = len(image[1])
	for i in range(h):
		for j in range(w):
			dist=pow(pow(j-circle[0],2)+pow(i-circle[1],2),0.5)
			if dist < circle[2]:
				onedim.append(image[i,j])

	return np.asarray(onedim)

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

