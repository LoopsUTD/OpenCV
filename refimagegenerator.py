"""
Script to generate reference images for spatial deviation analysis
"""
"""
OPERATION PARAMETERS - EDIT HERE DURING USE
"""
# Image size, in pixels
rsize = 600   # HEIGHT
csize = 400   # WIDTH

# Set one mode to True and the others to False
#   (If nothing is selected, blobs will be used)
#   (If multiple selected, lower takes precedence)
horizontalStripes = False
verticalStripes   = False
blobs             = True

# Set period of pattern, in pixels
period = 4

# If either orientation of stripes, set duty cycle
#   (If using blobs, ignore this line)
dutyCycle = 0.5

# If using blobs, set blob size
#   (If using stripes, ignore these lines)
rblob = 2     # HEIGHT OF BLOB (in px)
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
    if k == period:
        k = 0


"""
Display generated image
"""
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',csize,rsize)       # ("DisplayFrame",WIDTH,HEIGHT)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
=======
#!/usr/bin/env python

"""
Script to generate reference images for spatial deviation analysis
"""
import numpy as np
import cv2
import matplotlib as mat
"""
Image properties
"""
rsize=400
csize=400
period=2.0
dutycycle=0.5
cutoff=period*(dutycycle)
colorvect=np.array([[0,255,0]])
img=np.zeros((rsize,csize,3))
"""
Stripe addition
"""
k=0
for i in range(1,rsize):
    k=k+1
    if k<=cutoff:
        img[i,:,:]=np.dot(np.ones((csize,1)),colorvect)
    if k==period:
        k=0


"""
Display generated image

"""
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
>>>>>>> e10cd1e5f51e3a146badf2080b9054a4c549843d
=======
#!/usr/bin/env python

"""
Script to generate reference images for spatial deviation analysis
"""
import numpy as np
import cv2
import matplotlib as mat
"""
Image properties
"""
rsize=400
csize=400
period=2.0
dutycycle=0.5
cutoff=period*(dutycycle)
colorvect=np.array([[0,255,0]])
img=np.zeros((rsize,csize,3))
"""
Stripe addition
"""
k=0
for i in range(1,rsize):
    k=k+1
    if k<=cutoff:
        img[i,:,:]=np.dot(np.ones((csize,1)),colorvect)
    if k==period:
        k=0


"""
Display generated image

"""
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4