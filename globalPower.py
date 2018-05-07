import shapeFinder as lf
import blob				# the input array in demagnify uses the blob object from this file
import numpy as np		# The input array in demagnify is a numpy array

# Function calculatePower()
#  Given two cropped images of circles, one through the lens
#  and one without the lens, return the manifying power of the lens.
# INPUTS:
#  noLens - photo of LCD screen, without intervening lens, cropped to lens-sized region of interest
#  lens - photo of LCD screen, with intervening lens, cropped to lens-sized region of interest
# OUTPUTS:
#  power - floating-point number representing magnifying power of lens

def calculatePower(noLens,wLens):
	original = lf.findCircle(noLens)	# returns (x,y,r) of circle
	magnified = lf.findCircle(wLens)	# returns (x,y,r) of circle
	distLensToCamera = 0.3			# In meters, accurate within 0.03
	magnification = magnified[2]/original[2]
	power = (1 - magnified[2]/original[2])/distLensToCamera
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
		b.value[0] = (b.value[0]-lensCircle[0])/magnification + lensCircle[0]	# New X-position
		b.value[1] = (b.value[1]-lensCircle[1])/magnification + lensCircle[1]	# New Y-position
	return blobs