"""
-----------
Class Blob
-----------
This class is the base unit of data storage for the deviation maps.
Each blob represents an image segment found by a segmentation algorithm.
VARIABLE MEMBERS:
 - id - unique integer used to distinguish between blobs
 - x,y - coordinates of the blob's centroid in the source image, in pixels
FUNCTION MEMBERS:
 - __init__() - constructor
 - __str__() - defines a string that represents the object
"""

class Blob:
	def __init__(self,id,x,y):
		self.id=id
		self.value=[x,y]
	def __str__(self):
		return '{}{}'.format(self.id,self.value)