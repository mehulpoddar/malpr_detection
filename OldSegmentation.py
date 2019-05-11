import cv2
import numpy as np
import operator
import os

MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

class ContourWithData():

    npaContour = None
    boundingRect = None
    intRectX = 0
    intRectY = 0
    intRectWidth = 0
    intRectHeight = 0
    fltArea = 0.0

    def calculateRectTopLeftPointAndWidthAndHeight(self):               

        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):
        if self.fltArea < MIN_CONTOUR_AREA: return False  
        return True

def getDimen(x):
        [intX, intY, intWidth, intHeight] = x.boundingRect
        return (intWidth , intHeight)

def validSegmentation(allContoursWithData, limitWidth, limitHeight):
    classifiedContours = []

    for contourWithData in allContoursWithData:
        if contourWithData.fltArea > MIN_CONTOUR_AREA:
            dimen = getDimen(contourWithData)
            if len(classifiedContours)==0:
                classifiedContours.append([contourWithData])
                continue
            mean = []
            for contourClass in classifiedContours:
                DimenClass = list(map(getDimen,contourClass))
                classWidth = [ x[0] for x in DimenClass ]
                classHeight = [ x[1] for x in DimenClass ]
                meanWidthclass, meanHeightclass = np.mean(classWidth),np.mean(classHeight) 
                mean.append((meanWidthclass, meanHeightclass))
                
            done = 0
            for i,j in enumerate(mean):
                if (j[0]-limitWidth) <= dimen[0] <= (j[0]+limitHeight) and (j[1]-limitHeight) <= dimen[1] <= (j[1]+limitHeight):
                     classifiedContours[i].append(contourWithData)
                     done = 1
                     break
            if done == 0:
                classifiedContours.append([contourWithData])
                
    bigPos = 0
    for i,contourClass in enumerate(classifiedContours):
        if len(contourClass) > len(classifiedContours[bigPos]):
            bigPos = i

    if len(classifiedContours) == 0:
        return 'ignore'   
    return classifiedContours[bigPos]

def KNN(imgTestingNumbers, width, height):
    allContoursWithData = []
    validContoursWithData = []
    validCharacters = []
    
    imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)
    imgThresh = cv2.adaptiveThreshold(imgBlurred,
                                      255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV,
                                      11,
                                      2)
    imgThreshCopy = imgThresh.copy()
    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,
                                                 cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_SIMPLE)


    for npaContour in npaContours:                             
        contourWithData = ContourWithData()
        contourWithData.npaContour = npaContour
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)
        allContoursWithData.append(contourWithData)
        
    validContoursWithData = validSegmentation(allContoursWithData, width, height)

    if type(validContoursWithData) == type('ignore'):
        return 'ignore'

    validContoursWithData.sort(key = operator.attrgetter("intRectX"))
    

    for contourWithData in validContoursWithData:
        cv2.rectangle(imgTestingNumbers,
                      (contourWithData.intRectX, contourWithData.intRectY),
                      (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),
                      (0, 255, 0), 2)

        imgtoOCR = imgTestingNumbers[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                           contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]
        #cv2.imshow('segment',imgtoOCR)
        #cv2.waitKey(0)
        validCharacters.append(imgtoOCR)

    return validCharacters

def segment(imgPlate, resize = True):

    RESIZE_SIZE = 300
    ACCEPTANCE_LIMIT_H = 8
    ACCEPTANCE_LIMIT_W = 11

    if resize:
        h, w = imgPlate.shape[:2]
        ratio = w/h
        height = int(RESIZE_SIZE / ratio)
        imgPlate = cv2.resize(imgPlate, (RESIZE_SIZE, height))

    return KNN(imgPlate,ACCEPTANCE_LIMIT_W,ACCEPTANCE_LIMIT_H)
