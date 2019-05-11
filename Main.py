import numpy as np
import cv2
from pyimagesearch.transform import four_point_transform

import OCR
import Majority
import Segmentation
import OldSegmentation

def main():
    correctorOn = True
    oldSeg = False
    CNN_OCR = True

    plateImg = cv2.imread('./data/input/test5.png')
    height, width = plateImg.shape[:2]
    warped = four_point_transform(plateImg, np.array([(0,0),(width,0),(width,height),(0,height)]))
      
    if oldSeg:
    	validChars = OldSegmentation.segment(plateImg)
    else:
        validChars = Segmentation.startSegment(plateImg)
    print(str(len(validChars)))

    plateText = OCR.readPlate(validChars,correctorOn,CNN_OCR)
    if plateText != 'ignore':
       print(plateText)
    else:
       print('Try Again!')

main()
