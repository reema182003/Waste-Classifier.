import os
import cvzone
from cvzone.ClassificationModule import Classifier
import cv2
import serial
import time

# Initialize serial communication with Arduino
try:
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

cap = cv2.VideoCapture(0)
classifier = Classifier('Resources/Model/keras_model.h5', 'Resources/Model/labels.txt')
imgArrow = cv2.imread('Resources/arrow.png', cv2.IMREAD_UNCHANGED)
classIDBin = 0

# Import all the waste images
imgWasteList = []
pathFolderWaste = "Resources/Waste"
pathList = os.listdir(pathFolderWaste)
for path in pathList:
    imgWasteList.append(cv2.imread(os.path.join(pathFolderWaste, path), cv2.IMREAD_UNCHANGED))

# Import all the waste bin images
imgBinsList = []
pathFolderBins = "Resources/Bins"
pathList = os.listdir(pathFolderBins)
for path in pathList:
    imgBinsList.append(cv2.imread(os.path.join(pathFolderBins, path), cv2.IMREAD_UNCHANGED))

# 0 = Recyclable (index 0 in imgBinsList)
# 1 = Hazardous (index 1 in imgBinsList)
# 2 = Food (index 2 in imgBinsList)
# 3 = Residual (index 3 in imgBinsList)

classDic = {0: None,
            1: (0, 'R'),
            2: (0, 'R'),
            3: (3, 'N'),
            4: (3, 'N'),
            5: (1, 'H'),
            6: (1, 'H'),
            7: (2, 'F'),
            8: (2, 'F')}


def send_to_arduino(signal):
    print(f"Sending signal: {signal}")
    arduino.write(signal.encode())
    time.sleep(1)


while True:
    _, img = cap.read()
    imgResize = cv2.resize(img, (454, 340))

    imgBackground = cv2.imread('Resources/background.png')

    prediction = classifier.getPrediction(img)
    classID = prediction[1]
    print(f"Prediction: {prediction}, Class ID: {classID}")

    if classID != 0:
        imgBackground = cvzone.overlayPNG(imgBackground, imgWasteList[classID - 1], (909, 127))
        imgBackground = cvzone.overlayPNG(imgBackground, imgArrow, (978, 320))
        binIndex, signal = classDic[classID]
        if signal is not None:
            send_to_arduino(signal)
            imgBackground = cvzone.overlayPNG(imgBackground, imgBinsList[binIndex], (895, 374))

    imgBackground[148:148 + 340, 159:159 + 454] = imgResize

    # Displays
    cv2.imshow("Output", imgBackground)
    cv2.waitKey(1)