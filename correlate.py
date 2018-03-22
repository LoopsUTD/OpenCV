import cv2
import math
from blob import *
import numpy as np
from random import *
from math import *
def main(undeviated,deviated):
	print("main")
	undevdict={}
	devdict={}
	devmap=np.array([])
	for i in range(undeviated.size):
		undevdict.update({undeviated[i].id:undeviated[i]})
		closest=mindist(undeviated[i],deviated)
		devdict.update({closest.id:closest})
	for key,value in undevdict.items():
		dist=distance(value,devdict[key])
		deviation={dist:value.value}
		np.append(devmap,deviation)
		writeToFile(deviation,"dev.txt")

def writeToFile(mapping,name):
	file=open(name,"a")
	for value in mapping.items():
		file.write("{},{},{}\n".format(value[1][0],value[1][1],value[0]))
	file.close()
	
def testData(size,density):
	print("testData")
	undev=np.empty(density,dtype=Blob)
	dev=np.empty(density,dtype=Blob)
	for i in range(density):
		x=randint(1,size)
		y=randint(1,size)
		b=Blob(i,x,y)
		c=Blob(i+randint(0,density),x+randint(0,density/20),y+randint(0,density/20))
		undev.put(i,b)
		dev.put(i,c)
	return undev,dev

def mindist(item,array):
	minim=sys.maxsize
	for i in range(array.size):
		idist=distance(item,array[i])
		if idist < minim:
			mindist=idist
			closest=array[i]
			closest.id=item.id
	return closest
	
def distance(blob1,blob2):
	dist=sqrt(math.pow((blob1.value[0]-blob2.value[0]),2)+math.pow((blob1.value[1]-blob2.value[1]),2))
	return dist
if __name__=='__main__':
	
	print("isit")
	data=testData(1000,1000)
	main(data[0],data[1])

