from PIL import Image
import pytesseract
import cv2
import os
import sys
import re
import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
import _thread as t

import Majority
import Corrector

finalString = []
chars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C',
            'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def readCharCNN(img,model):
        global finalString, chars

        '''h, w = image.shape[:2]
        ratio = w/h
        
        width = int(100 * ratio)
        resizedImg = cv2.resize(image, (width, 100))'''

        #cv2.imshow('yolo', img)
        #cv2.waitKey(0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        img = cv2.resize(img, (100,100))
        img = np.expand_dims(img, axis=2)
        img = np.expand_dims(img, axis=0)

        res = list(model.predict(img)[0])

        if 1. in res:
        	finalString.append(chars[res.index(1.)])
        else:
                finalString.append('')

def readCharTes(image,pos):
        global finalString

        possibleChars = []
        charMem = ''

        h, w = image.shape[:2]
        ratio = w/h
        
        for width in [700,1400,1100,900]:
                height = int(width / ratio)
                resizedImg = cv2.resize(image, (width, height))

                preimage = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
                preimage = cv2.threshold(preimage, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                preimage = cv2.medianBlur(preimage, 3)
                preimage = Image.fromarray(preimage)

                try:
                        possibleChar = pytesseract.image_to_string(preimage, config = '--psm 10')
                        if possibleChar.isalnum():
                                possibleChars.append(possibleChar)
                                if charMem == possibleChar and charMem != '':
                                        break
                                charMem = possibleChar            
                except UnicodeEncodeError:
                        pass

        if len(possibleChars) != 0:

                majorityIndex = Majority.pickFrom(possibleChars)
                finalString[pos] = possibleChars[majorityIndex]
                print(possibleChars[majorityIndex])
        else:
                finalString[pos] = ''

def readPlate(validChars,correctorOn, CNN_OCR):
        global finalString

        if not (5 < len(validChars) < 12):
                return 'ignore'

        if CNN_OCR:
                model = Sequential()

                model.add(Conv2D(
                filters = 32,
                kernel_size=(4,4),
                strides = 1,
                activation = 'relu',
                input_shape = (100, 100, 1)
                ))
                
                model.add(Conv2D(
                        filters = 32,
                        kernel_size=(4,4),
                        strides = 1,
                        activation = 'relu'
                        ))
                
                model.add(MaxPooling2D(pool_size=(2,2)))
                model.add(Dropout(0.25))

                model.add(Conv2D(
                filters = 32,
                kernel_size=(4,4),
                strides = 1,
                activation = 'relu'
                ))
                
                model.add(Conv2D(
                        filters = 32,
                        kernel_size=(4,4),
                        strides = 1,
                        activation = 'relu'
                        ))
                
                model.add(MaxPooling2D(pool_size=(2,2)))
                model.add(Dropout(0.25))

                model.add(Flatten())
                model.add(Dense(units = 256, activation = 'relu'))
                model.add(Dropout(0.5))
                model.add(Dense(units = 36, activation = 'softmax'))

                # Compiling the Model
                model.compile(optimizer='rmsprop',
                              loss='categorical_crossentropy',
                              metrics=['accuracy'])

                model.load_weights('weights.h5')
                
                for char in validChars:
                        readCharCNN(char,model)

                K.clear_session()

        else:
                pos = 0

                try:
                    for char in validChars:
                         finalString.append('nil')
                         t.start_new_thread(readCharTes, (char,pos))
                         pos += 1

                    flag = True
                    while flag:
                         flag = False
                         for ch in finalString:
                             if ch == '':
                                 return 'ignore'
                             if ch == 'nil':
                                 flag = True
                except UnicodeEncodeError:
                    pass

        print(finalString)
        if finalString != []:
            if correctorOn:
                finalStr = Corrector.correct(''.join(finalString))
            else:
                finalStr = ''.join(finalString)
            if  re.match(r'[A-Z][A-Z]\d\d', finalStr):
                return finalStr
        return 'ignore'
