#!/usr/bin/env python

"""
"""
import numpy as np
import cv2
import matplotlib as mat

img=np.zeros((200,200))
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
