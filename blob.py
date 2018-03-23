import sys

def main():
	if len(sys.argv)==1:
		blob1=Blob(0,0,0)
	else:
		blob1=Blob(sys.argv[1],sys.argv[2],sys.argv[3])
	print(blob1.id)
	print(blob1.value)

class Blob:
	def __init__(self,id,x,y):
		self.id=id
		self.value=[x,y]

if __name__ == '__main__':
	main()