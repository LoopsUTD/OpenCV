import numpy as np
from blob import *
from random import *
def testData(size,density):
	print("testData")
	undev=np.empty(density,dtype=Blob)
	dev=np.empty(density,dtype=Blob)
	for i in range(density):
		x=randint(0,size)
		y=randint(0,size)
		b=Blob(i,x,y)
		c=Blob(i+randint(0,density),x+randint(density/-20,density/20),y+randint(density/-20,density/20))
		undev.put(i,b)
		dev.put(i,c)
	return undev,dev


