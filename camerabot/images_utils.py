# import the necessary packages
from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity
import argparse
import imutils
import cv2
from typing import Dict, List, Tuple

from os import sys, path
sys.path.append(path.dirname(path.abspath(__file__)))
import file_utils


import numpy as np
import tempfile
import glob

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--first", required=True,
#     help="first input image")
# ap.add_argument("-s", "--second", required=True,
#     help="second")
# args = vars(ap.parse_args())

# # load the two input images
# imageA = cv2.imread(args["first"])
# imageB = cv2.imread(args["second"])


def compare_two_images_1():
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    boxes = []
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        boxes.append([w*h, [x,y,w,h]])

    for area,[x,y,w,h] in sorted(boxes)[-10:]: 
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # show the output images
    cv2.imwrite("Original.jpg", imageA, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    cv2.imwrite("Modified.jpg", imageB, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    cv2.imwrite("Diff.jpg", diff, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    cv2.imwrite('3.jpg', imageA, [int(cv2.IMWRITE_JPEG_QUALITY), 80]) 
    cv2.imwrite("Thresh.jpg", thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    # cv2.waitKey(0)

#-------------------------------------------------------------------------------------------------------------------
def compare_two_images_2():
    original = imutils.resize(imageA, height = 600)
    new = imutils.resize(imageB, height = 600)

    #make a copy of original image so that we can store the
    #difference of 2 images in the same
    diff = original.copy()
    cv2.absdiff(original, new, diff)

    
    #converting the difference into grascale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('gray',gray)
    cv2.waitKey(0)
 
    #increasing the size of differences so we can capture them all
    for i in range(0, 1):
        dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)

    cv2.imshow('dilated',dilated)
    cv2.waitKey(0)

    #threshold the gray image to binarise it. Anything pixel that has
    #value more than 3 we are converting to white
    #(remember 0 is black and 255 is absolute white)
    #the image is called binarised as any value less than 3 will be 0 and
    # all values equal to and more than 3 will be 255
    (T, thresh) = cv2.threshold(dilated, 30, 255, cv2.THRESH_BINARY)

    cv2.imshow('thresh',thresh)
    cv2.waitKey(0)
     
    # now we need to find contours in the binarised image
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)



    for c in cnts:
        # fit a bounding box to the contour
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
    #uncomment below 2 lines if you want to
    #view the image press any key to continue
    #write the identified changes to disk
    cv2.imshow('new',new)
    cv2.waitKey(0)
    cv2.imwrite("changes.png", new)


#-----------------------------------------------------------------------------------------------------
def get_ss_score(file1: str, file2: str) -> float:
    """ Compute  the mean structural similarity index between two images. """
    imageA = cv2.imread(file1)
    imageB = cv2.imread(file2)
    original = imutils.resize(imageA, height = 600)
    new = imutils.resize(imageB, height = 600)
    grayA = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(grayA, grayB, full=True)
    return score


#-----------------------------------------------------------------------------------------------------
def compare_two_images_3(ObjFileName: str, RefFileName: str, fileOut=None) -> str:
    """ Compares two images and return image with boxes """
    
    # show only boxes w/ area larger than (px^2):
    AREA_TRESHOLD = 10000
    
    imageA = cv2.imread(ObjFileName)
    imageB = cv2.imread(RefFileName)
    
    original = imutils.resize(imageA, height = 600)
    new = imutils.resize(imageB, height = 600)
    #original = imageA
    #new = imageB

    grayA = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)


    #make a copy of original image so that we can store the
    #difference of 2 images in the same
    diff = original.copy()
    cv2.absdiff(original, new, diff)


    #converting the difference into grascale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(grayA, grayB, full=True)
 
    #increasing the size of differences so we can capture them all
    for i in range(0, 3):
        dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)

    #threshold the gray image to binarise it. Anything pixel that has
    #value more than 3 we are converting to white
    #(remember 0 is black and 255 is absolute white)
    #the image is called binarised as any value less than 3 will be 0 and
    # all values equal to and more than 3 will be 255
    (T, thresh) = cv2.threshold(dilated, 20, 255, cv2.THRESH_BINARY)
     
    # now we need to find contours in the binarised image
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    #lets sort by rectangle size
    boxes = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        boxes.append([w*h, [x,y,w,h]])
    boxes.sort(reverse=True)

    for area,[x,y,w,h] in boxes[:10]: 
        if  area>AREA_TRESHOLD:
            #cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # if the output file is not specified, creata temporary file
    if not fileOut:
        fileOutFD, fileOut = tempfile.mkstemp(suffix='.jpg')
        print (fileOut)
    
    cv2.imwrite(fileOut, original, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

    1/0
    return fileOut

def blendImages(files: List[str], saveAs: str):
    
    print('Blending...')
    image_data = list()
    for my_file in files:
        this_image = cv2.imread(my_file, 1)
        this_image = imutils.resize(this_image, height = 600)
        image_data.append(this_image)
     
    # Calculate blended image
    dst = image_data[0]
    for i in range(len(image_data)):
        if i == 0:
            pass
        else:
            alpha = 1.0/(i + 1)
            beta = 1.0 - alpha
            dst = cv2.addWeighted(image_data[i], alpha, dst, beta, 0.0)
            print(f'Blending {i} of {len(image_data)}')
    #save as
    cv2.imwrite(saveAs, dst, [int(cv2.IMWRITE_JPEG_QUALITY), 80])


def test_blend():
    pathToPics = r'/Users/sash/mnt/zavulon_pub/cam_motion/Entrance/2020_04_13-2020_05_12'
    listOfFiles = glob.glob(pathToPics + r'/*.jpg') 
    blendImages(listOfFiles, 'blended.jpg')

def main():
    fileLists = file_utils.groupPicsByTime()

    for index, groupCur in enumerate(fileLists[-2:]):

        #blendImages(groupCur, f'{index}_blended.jpg')
        # continue
        # N = len(groupCur)
        # if N < 2: continue
        # score = [] 
        # for i in range(N):
        #     for j in range(i+1, N):
        #         score.append([get_ss_score(groupCur[i], groupCur[j]), i , j])

        # minScore , iMin, jMin = min(score)
        # print(f'N={N} min score={minScore}')




        fileOut = 'out_{}.jpg'.format(index)
        compare_two_images_3(groupCur[0], groupCur[-1],fileOut)
        # print('\n'.join([','.join(map(lambda x: f' {x[0]:.2f}',row)) for row in score]))
        # print (score)


if __name__ == '__main__':
    #main()
    test_blend()






