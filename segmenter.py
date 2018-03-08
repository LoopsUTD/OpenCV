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
    cv2.imshow("greenscale",image)
    cv2.imwrite('segmented.png',image)
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
            a[...] = 10000
        else:
            a[...] = -10000
    return image

# INPUT:  Thresholded image
# OUTPUT: Image with isolated segments

def segment(image):
    index = 1
    h = len(image)
    w = len(image[1])

    for i in range(1,h-1):
        for j in range(1,w-1):
#     for i in range(h-1):
#         for j in range(w-1):
            if image[i,j] >= 1:
                a = index
                if image[i-1,j] > 0 and image[i-1,j] < a:
                    a = image[i-1,j]
                if image[i+1,j] > 0 and image[i+1,j] < a:
                    a = image[i+1,j]
                if image[i,j-1] > 0 and image[i,j-1] < a:
                    a = image[i,j-1]
                if image[i,j+1] > 0 and image[i,j+1] < a:
                    a = image[i,j+1]
                if a == index:
                    index = index+1
                image[i,j] = a
    print(image)
    print(index)
    return image

if __name__ == '__main__':
    # this image name is not important.  I was just using what I had on my computer
    extractObjects('test.jpg')   