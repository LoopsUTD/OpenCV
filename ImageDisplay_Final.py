import numpy as np
import cv2
cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
im = cv2.imread("DSC03113.jpg")                     # Read image
imS = cv2.resize(im, (1280, 1024))                    # Resize image
cv2.imshow("output", imS)                           # Show image
cv2.moveWindow("output", 1920,-5)
cv2.waitKey(0)
   

