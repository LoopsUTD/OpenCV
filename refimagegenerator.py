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
