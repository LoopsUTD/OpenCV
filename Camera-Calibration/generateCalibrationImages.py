import tkinter
import numpy
import cv2
import imageDisplay

# INPUT: 'calib.png', the name of the checkerboard/calibration image, as a string
# OUTPUT: filenames, array containing names of the 16 images captured
# FILE I/O: saves 16 images

def generateCalibrationImages(refImage):
    rootWindow   = tkinter.Tk()
    screenWidth  = rootWindow.winfo_screenwidth()
    screenHeight = rootWindow.winfo_screenheight()

    board = cv2.imread(refImage)
    boardHeight, boardWidth = board.shape[:2]

    positions = numpy.zeros((16,2))
    filenames = list()  # will contain 16 image file names

    for i in range(0,4):
        for j in range(0,4):
            positions[4*i+j,0] = i * (screenHeight - boardHeight)/3
            positions[4*i+j,1] = j * (screenWidth - boardWidth)/3

    print(positions)

    for i in range(0,16):
        #capture jpgs if that will generate sufficient results
        imageDisplay.display(refImage, int(positions[i,1]), int(positions[i,0]))
        #filename = captureImage()
        #filenames[i] = filename

    return filenames

if __name__ == '__main__':
    # this image name is not important.  I was just using what I had on my computer
    print(generateCalibrationImages("dragon_turtle.jpg"))