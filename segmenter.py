import cv2
import numpy
from blob import Blob

# INPUT:  name of .png photograph file
# OUTPUT: array of found blob objects
# FILE I/O: loads image from file of given name

def extractObjects(filename):
    image = cv2.imread(filename)
    cv2.imshow("greenscale",image)
    cv2.waitKey(0)
    image = greenscale(image)
    cv2.imshow("greenscale",image)
    cv2.waitKey(0)
    thresh = 64
    image = threshold(image,thresh)
    cv2.imshow("greenscale",image)
    cv2.waitKey(0)
    image = segment(image)
    cv2.imshow("greenscale",image.astype(dtype='uint8'))
    cv2.waitKey(0)
    foundBlobs = segmentInfo(image)    
    cv2.imwrite("output.png",image.astype(dtype='uint8'))
    return foundBlobs

# Sub-functions

# INPUT:  array representation of image, 1- or 3-channel
# OUTPUT: 1-channel representation of image
# Instead of true greyscale, we use greenscale(since all test images are green)

def greenscale(image):
    channels = len(image.shape)
    if channels == 1:
        image = image
    elif channels == 3:
        image = image[:,:,2]
    else:
        print("Error in segmentImg >> greenscale: image is not 1- or 3-channel")
        image = numpy.zeros(2,2)
    return image

# INPUT:  1-channel array representing an image
# OUTPUT: Array containing only -10,000 (low values) or 10000 (high values) in each entry

def threshold(image,thresh):
    for a in numpy.nditer(image, op_flags=['readwrite']):
        if a >= thresh:
            a[...] = 255
        else:
            a[...] = 0
    return image

# INPUT:  Pixel location of part of blob\
# TASK:   Recursively "Fills" a blob from one found pixel
# OUTPUT: None per se, but it checks all neighbors

def fill(image,i,j,h,w,index):
    image[i,j] = index
    if i > 0 and image[i-1,j] == 255:
        fill(image,i-1,j,h,w,index)
    if i+1 < h and image[i+1,j] == 255:
        fill(image,i+1,j,h,w,index)
    if j > 0 and image[i,j-1] == 255:
        fill(image,i,j-1,h,w,index)
    if j+1 < w and image[i,j+1] == 255:
        fill(image,i,j+1,h,w,index)
    return

# INPUT:  Thresholded image
# OUTPUT: Image with isolated segments

def segment(image):
    index = 256     # Starts at 256 because the largest number in the image will be 255
    h = len(image)
    w = len(image[1])
    image = image.astype(dtype='uint16')
    
    for i in range(h):
        for j in range(w):
            if image[i,j] > 0 and image[i,j] < 256:     # if the pixel is part of an object and not yet marked
                fill(image,i,j,h,w,index)
                index = index + 1
                
    print(index-256)
    return image

# INPUT:  Image with isolated and labeled segments
# OUTPUT: Array of blob objects

def segmentInfo(img):
    h = len(img)
    w = len(img[1])
    b = {}
    
    for i in range(h):
        for j in range(w):
            if img[i,j] != 0:
                if img[i,j] not in b:
                    b[img[i,j]] = [1,i,j]
                else:
                    b[img[i,j]] = [b[img[i,j]][0]+1,b[img[i,j]][1]+i,b[img[i,j]][2]+j]
    print(b)
                    
    blobs = list()
    for key in b:
        ssn = key
        x   = b[key][1] / b[key][0]
        y   = b[key][2] / b[key][0]
        newBlob = Blob(ssn,x,y)
        blobs.append(newBlob)
    return blobs

if __name__ == '__main__':
    # this image name is not important.  I was just using what I had on my computer
    extractObjects('test.png')   