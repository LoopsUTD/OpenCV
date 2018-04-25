import lensFinder as lf
import blob
import numpy as np

# Function calculatePower()
#  Given two cropped images of circles, one through the lens
#  and one without the lens, return the manifying power of the lens.
# INPUTS:
#  noLens - photo of LCD screen, without intervening lens, cropped to lens-sized region of interest
#  lens - photo of LCD screen, with intervening lens, cropped to lens-sized region of interest
# OUTPUTS:
#  power - floating-point number representing magnifying power of lens

def calculatePower(noLens,wLens):
	original = lf.findLens(noLens)
	magnified = lf.findLens(wLens)
	distLensToCamera = 0.3			# In meters, accurate within 0.03
	magnification = magnified/original
	power = (1 - magnified/original)/distLensToCamera
	return magnification, power

# Function demagnify()
#  Given a list of blobs moved by magnification, a center-of-magnification location, and a magnifying factor,
#  returns an un-magnified version of the list
# INPUTS:
#  blobs - numpy array of blob objects in the distorted (magnified) image
#  lensCircle - region of interest, the center is used for demagnification calculations
#  magnification - ratio of magnified size to unmagnified size
# OUTPUTS:
#  deMagBlobs - numpy array of blobs with de-magnified positions

def demagnify(blobs,lensCircle,magnification):
	blobs = blobs.copy()
	for b in blobs:
		b.value[0] = (b.value[0]-lensCircle[0])/magnification + b.value[0]	# New X-position
		b.value[1] = (b.value[1]-lensCircle[1])/magnification + b.value[1]	# New Y-position
	return blobs