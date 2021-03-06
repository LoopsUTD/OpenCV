from blob import *
import numpy as np
from math import *
import os.path
from time import *
from multiprocessing import *
import sys
"""
This script takes in two numpy arrays containing the 
centroids and ids of the blobs in the deviated and undeviated images. It finds the pairs of blobs with the shortest distance between them and stores that distance as the deviation value at the position of the undeviated blob.
"""

#INPUT: 2 x numpy arrays corresponding to segmented blob positions, output directory, name of lens
#OUTPUT: python dictionary containing an entry for every blob with a partner, of the form {(xposition, yposition):distance}
#FILE I/O: writes .txt file containing the output dictionary to output directory
def main(undeviated,deviated,dirname,name):

	fname="{}/{}{}".format(dirname,name,".txt")
#	if(os.path.isfile(fname)):
#		os.remove(fname)
	undevdict,devdict=corr(undeviated,deviated)
	devmap=compare(undevdict,devdict)
	writeToFile(devmap,fname)
	return devmap	

def compare(undevdict,devdict):
	devmap={}
	for key,value in undevdict.items():
		dist=sqrt(distanceSquared(value,devdict[key]))
		deviation={(value.value[0],value.value[1]):dist}
		devmap.update(deviation)
	return devmap

def corr(undeviated,deviated):
	undevdict={}
	devdict={}
	for i in range(undeviated.size):
		undevdict.update({undeviated[i].id:undeviated[i]})
		closest=minDistSquared(undeviated[i],deviated)
		devdict.update({closest.id:closest})
	return undevdict,devdict

def writeToFile(mapping,name):
	file=open(name,"w")
	for value in mapping.items():
		line=("{},{},{}\n".format(value[0][0],value[0][1],value[1]))
		file.write(line)
	file.close()
	
def minDistSquared(item,array):
	minim=sys.maxsize
	for i in range(array.size):
		idist=distanceSquared(item,array[i])
		if idist < minim:
			minim=idist
			closest=array[i]
			closest.id=item.id
	return closest
	
def distanceSquared(blob1,blob2):
	distSquared=pow((blob1.value[0]-blob2.value[0]),2)+pow((blob1.value[1]-blob2.value[1]),2)
	return distSquared

if __name__=='__main__':
	print("main")
	start = time()
	data=testData(5000,3000)
	main(data[0],data[1])
	print(time()-start)
