import lensFinder as lf

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
	distLensToCamera = 0.3			# In meters, needs to be measured.
	power = (1 - magnified/original)/distLensToCamera
	return power