"""
Script to generate reference images for spatial deviation analysis
"""

"""
OPERATION PARAMETERS - EDIT HERE DURING USE
"""

# Image size, in pixels
rsize = 900	 # HEIGHT
csize = 1920     # WIDTH

# Set one mode to True and the others to False
#   (If nothing is selected, blobs will be used)
#   (If multiple selected, lower takes precedence)
horizontalStripes = False
verticalStripes   = False
checkerboard      = False
blobs             = True

# Set period of pattern, in pixels
period = 4

# If either orientation of stripes, set duty cycle
#   (If using blobs, ignore this line)
dutyCycle = 0.5

# If using blobs, set blob size
#   (If using stripes, ignore these lines)
rblob = 1     # HEIGHT OF BLOB (in px)
cblob = 1     # WIDTH OF BLOB (in px)

"""
END OF OPERATION PARAMETERS - EDITING BELOW THIS POINT MAY BREAK THINGS
"""

"""
Dependencies
"""
import numpy as np
import cv2

"""
Variable Declarations
"""

if blobs:
    rb = rblob
    cb = cblob
elif verticalStripes:
    rb = period
    cb = dutyCycle*period
elif horizontalStripes:
    rb = dutyCycle*period
    cb = period
elif checkerboard:
    rb=period/2
    cb=period/2    
else:
    print("No Mode Selected, attempting to generate 2x2 blobs with period 4")
    rb = 2
    cb = 2
    period = 4

colorvect = np.array([[0,255,0]])   # Sets color of powered pixel, currently GREEN
img = np.zeros((rsize,csize,3))

"""
Feature Addition
"""

k = 0
for i in range(1,rsize):
    k = k + 1
    if k <= rb:
        m = 0
        for j in range(1,csize):
            m = m + 1
            if m <= cb:
                img[i,j,:] = colorvect
            if m == period:
                m = 0
    if checkerboard and k > rb:
        m = 0
        for j in range(1,csize):
            m = m + 1
            if m > cb:
                img[i,j,:] = colorvect
            if m == period:
                m = 0
        
    if k == period:
        k = 0

"""
Save Image
"""

cv2.imwrite('test.png',img)

"""
Display generated image
"""

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',csize,rsize)
# ("DisplayFrame",WIDTH,HEIGHT)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()