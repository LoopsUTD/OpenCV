import segmenter
import correlate
from time import *
if __name__=="__main__":	
	start=time()
	undevname="lens2_nolens_4pxG.png"
	devname="lens2_wlens_4pxG.png"
#j	undevname="undevdumb.png"
#	devname="devdumb.png"
	undev=segmenter.extractObjectsPngJpg(undevname)
	print('undev done')
	print (time()-start)
#	for blobs in undev:
#		print("u")
#		print(blobs)
	dev=segmenter.extractObjectsPngJpg(devname)
	print('dev done')
	print (time()-start)
#	for blobs in dev:
#		print("d")
#		print(blobs)
	correlate.main(undev,dev)
	print (time()-start)
