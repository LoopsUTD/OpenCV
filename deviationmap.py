import numpy
import blob


def main():
	map = [[blob.Blob(j*i+j, j, i) for i in range(600)] for j in range(400)]
	for rows in map:
		for blobs in rows:
			print(str(blobs.id)+" "+str(blobs.value))
if __name__ == '__main__':
	main()
