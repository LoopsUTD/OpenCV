import numpy as np
import blob


class deviationMap:
	def __init__(self,original,deviated):
		self.deviation=difference(original,deviation)

	def difference(original, deviated):
		return deviated-original
def main():
	map = [[blob.Blob(600*(i)+j, i, j) for j in range(600)] for i in range(400)]
	for rows in map:
		for blobs in rows:
			print(str(blobs.id)+" "+str(blobs.value))
if __name__ == '__main__':
	main()
