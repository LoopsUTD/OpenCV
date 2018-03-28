import segmenter
import correlate
from time import *
if __name__=="__main__":	
	start=time()
#	undevname="lens2_nolens_4pxG.png"
#	devname="lens2_wlens_4pxG.png"i
	name='blank'
	imagefolder="../JPG_ADJUSTED_SIZE/"
	undevname='{}{}{}'.format(imagefolder,name,"_nolens.JPG")
	devname='{}{}{}'.format(imagefolder,name,"_lens.JPG")
	print(undevname,devname)
	undev=segmenter.extractObjectsPngJpg(undevname)

	print('undev segmented')
	print(time()-start)
#	for blobs in undev:
#		print("u")
#		print(blobs)
	dev=segmenter.extractObjectsPngJpg(devname,64)
	print('dev segmented')
	print(time()-start)
#	for blobs in dev:
#		print("d")
#		print(blobs)
	correlate.main(undev,dev,name)
	print ('Total time elapsed: {} seconds'.format(time()-start))
