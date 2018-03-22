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
	print(undeviated)
	for i in range(undeviated.size):
		undevdict.update({undeviated[i].id:undeviated[i]})
		closest=mindist(undeviated[i],deviated)
		devdict.update({closest.id:closest})
	for key,value in undevdict.items():
		dist=distance(value,devdict[key])
		deviation={key:(dist,value.value)}
		np.append(devmap,deviation)
		print(deviation)
	
def testData(size):
	print("testData")
	data=np.empty(size,dtype=Blob)
	for i in range(size):
		b=Blob(i,randint(1,1000),randint(1,1000))
		print(b.value)
		print(data[i])
		data.put(i,b)
	return data

def mindist(item,array):
	print("mindist")
	minim=sys.maxsize
	for i in range(array.size):
		idist=distance(item,array[i])
		if idist < minim:
			mindist=idist
			closest=array[i]
			closest.id=item.id
	return closest
	
def distance(blob1,blob2):
	print("distance")
	dist=sqrt(math.pow((blob1.value[0]-blob2.value[0]),2)+math.pow((blob1.value[1]-blob2.value[1]),2))
	return dist
if __name__=='__main__':
	
	print("isit")
	main(testData(10),testData(10))

