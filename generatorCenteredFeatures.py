import cv2

# - - - - - - - - - - - #
# Function filledCircle
# - - - - - - - - - - - #
#   Draws a filled circle 
#   in an image at a specified 
#   location
# Input:
#   x - x position of center
#   y - y position of center
#   r - radius of circle
#   img - 8-bit integer matrix
# - - - - - - - - - - - #

def filledCircle(x,y,r,img)
	maxDist = r*r
	for i,j in img
		if (i-x)**2 + (j-y)**2 <= maxDist:
			img[i,j] = 256
	return img 