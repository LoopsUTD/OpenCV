import segmenter
import correlate
if __name__=="__main__":	
	undevname="lens2_nolens_280pxG.png"
	devname="lens2_wlens_280pxG.png"
	undev=segmenter.loudExtractObjectsPngJpg(undevname)
	print('undev done')
	dev=segmenter.loudExtractObjectsPngJpg(devname)
	print('dev done')
	correlate.main(undev,dev)
