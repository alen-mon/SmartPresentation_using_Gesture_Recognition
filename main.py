import cv2
from cvzone.HandTrackingModule import HandDetector
import os
import numpy as np
import time
import sys

# Get the arguments passed to the script
args = sys.argv

IpcameraVariable = ''
if args[1] == "0":
    IpcameraVariable = 0
else:
    IpcameraVariable = args[1]
    IpcameraVariable = str(IpcameraVariable)
print("Camera Feed:" + IpcameraVariable)
# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "Presentation"

blueLower = (100, 60, 60)
blueUpper = (140, 255, 255)

# Camera Setup
cap = cv2.VideoCapture(IpcameraVariable)
cap.set(3, width)
cap.set(4, height)
cv2.namedWindow("FullScreen", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("FullScreen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image
hb, wb = int(120 * 3), int(213 * 3)
# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

buttonTogglePressed = False

while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)

    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw

    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 5)

    if hands and buttonPressed is False:  # If hand is detected

        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal
        if (cx <= 100 & cy <= 100):
            time.sleep(1)
            buttonTogglePressed = not buttonTogglePressed;

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    h, w, _ = imgCurrent.shape

    if (buttonTogglePressed == False):
        imgSmall = cv2.resize(img, (ws, hs))
        imgCurrent[0:hs, w - ws: w] = imgSmall
    else:
        imgnew = cv2.resize(img, (wb, hb))
        imgCurrent[0:hb, w - wb: w] = imgnew

    cv2.imshow("FullScreen", imgCurrent)
    # cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
