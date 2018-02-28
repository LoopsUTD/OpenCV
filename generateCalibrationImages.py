import tkinter
import numpy
import cv2

# INPUT: 'calib.png', the name of the checkerboard/calibration image, as a string
# OUTPUT: filenames, array containing names of the 16 images captured
# FILE I/O: saves 16 images

def generateCalibrationImages():
    rootWindow   = tkinter.Tk()
    screenWidth  = rootWindow.winfo_screenWidth()
    screenHeight = rootWindow.winfo_screenHeight()

    board = cv2.imread('calib.png')
    boardHeight, boardWidth, boardChannels = board.shape

    positions = numpy.zeros((16,2))
    filenames = [16]

    for i in range(0,3):
        for j in range(0,3):
            positions[4*i+j,0] = i * (screenWidth - boardWidth)/3
            positions[4*i+j,1] = j * (screenHeight - boardHeight)/3

    for i in range(0,16):
        #displayImage(board, positions[i,0], positions[i,1]
        #captureImage
        #saveImage, grab filename
        filenames[i] = filename

    return filenames