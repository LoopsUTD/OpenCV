import sys
"""
This class is the base unit of data storage for the deviation maps. Each blob is a segmented pixel which stores centroid and ID. 
"""
class Blob:
	def __init__(self,id,x,y):
		self.id=id
		self.value=[x,y]
	def __str__(self):
		return '{}{}'.format(self.id,self.value)

