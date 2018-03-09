import cv2
import numpy

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
    thresh = 128
    image = threshold(image,thresh)
    cv2.imshow("greenscale",image)
    cv2.waitKey(0)
    image = segment(image)
    cv2.imshow("greenscale",image.astype(dtype='uint8'))
    cv2.waitKey(0)

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

# INPUT:  Thresholded image
# OUTPUT: Image with isolated segments

def segment(image):
    index = 1
    h = len(image)
    w = len(image[1])
    image = image.astype(dtype='uint16')

    for i in range(h):
        for j in range(w):
            if image[i,j] > 0:
                a = index
                if i > 0 and image[i-1,j] and a > image[i-1,j]:
                    a = image[i-1,j]
#                 if i < h - 1 and image[i+1,j] and a > image[i+1,j]:
#                     a = image[i+1,j]
                if j > 0 and image[i,j-1] and a > image[i,j-1]:
                    a = image[i,j-1]
#                 if j < w - 1 and image[i,j+1] and a > image[i,j+1]:
#                     a = image[i,j+1]
                if a == index:
                    index = index + 1
                image[i,j] = a
    print(index)
    return image

if __name__ == '__main__':
    # this image name is not important.  I was just using what I had on my computer
    extractObjects('test.jpg')   