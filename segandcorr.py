import segmenter
import correlate
if __name__=="__main__":	
	undevname="clens2_nolens.png"
	devname="clens2_wlens.png"
#j	undevname="undevdumb.png"
#	devname="devdumb.png"
	undev=segmenter.extractObjectsPngJpg(undevname)
	print('undev done')
	for blobs in undev:
		print("u")
		print(blobs)
	dev=segmenter.extractObjectsPngJpg(devname)
	print('dev done')
	for blobs in dev:
		print("d")
		print(blobs)

