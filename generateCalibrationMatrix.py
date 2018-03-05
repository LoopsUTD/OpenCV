import numpy
import cv2

# INPUT: filenames, array containing names of the 16 images captured
# OUTPUT: cameraMatrix, small 2-D array containing undistortion parameters
# FILE I/O: loads 16 images, one at a time

def generateCalibrationMatrix(filenames):
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # relative physical position template for 7x7 grid of chessboard interior corners
    # needs to be converted to millimeters
    grid = numpy.zeros((7*7,3), numpy.float32)
    grid[:,:2] = numpy.mgrid[0:7,0:7].T.reshape(-1,2) # Makes first two columns into all possible ordered pairs in [0,6] X [0,6]
    
    physpoints = [] # points in 3d physical space
    imgpoints = [] # points in 2d image space
    
    for file in filenames:
        image = cv2.imread(file)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        
        found, corners = cv2.findChessboardCorners(image, (7,7),None)
        if found == True:
            physpoints.append(grid)  # can be adjusted for moving position of images
                                    # but that might not actually matter
            corners = cv2.cornerSubPix(image,corners,(11,11),(-1,-1),criteria)  # refines corners, may not be necessary
            imgpoints.append(corners)
            
    success, calibrationMatrix = cv2.calibrateCamera(physpoints, imgpoints, image.shape[::-1],None,None)
    # If more information is required or would be useful, use below statement to catch it
    # success, calibrationMatrix, distortionCoefficients, rotationVectors, translationVectors = cv2.calibrateCamera(physpoints, imgpoints, image.shape[::-1],None,None)
    
    if success == True:
        return calibrationMatrix
    
    return -1 * numpy.identity(4)