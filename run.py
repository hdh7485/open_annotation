import cv2
import numpy as np
import math

refPt = []
candidateContours = []
candidateRectangles = []

rawImage = cv2.imread("narrow_path_1.jpg")
blurImage = cv2.bilateralFilter(rawImage, 3, 75, 75)
grayImage = cv2.cvtColor(blurImage, cv2.COLOR_BGR2GRAY)
cannyImage = cv2.Canny(grayImage, 150, 250, 3)

image, contours, hierachy = cv2.findContours(cannyImage, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contourImage = cv2.drawContours(rawImage, contours, -1, (255,255,255), 1)

print(hierachy)

displayImage = rawImage.copy()

# Straight Rectangle
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    height, width, channels = rawImage.shape
    if height/15 < h and width/15 < w:
        cv2.rectangle(displayImage,(x,y),(x+w, y+h),(0,0,255), 1)
        candidateContours.append(cnt)
        candidateRectangles.append((x,y,w,h))
#print(candidateContours)

def euclidian_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def click_and_crop(event, x, y, flags, param):
    global refPt 
    global candidateContours 
    global candidateRectangles

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        print(refPt)

        nearestPoint = 10000
        nearestRectangle = candidateRectangles[0]
        tempPoint = 0

        for rect in candidateRectangles:
            tempPoint = euclidian_distance(rect[0], rect[1], x, y)
            if tempPoint < nearestPoint:
                nearestPoint = tempPoint
                nearestRectangle=rect

            tempPoint = euclidian_distance(rect[0]+rect[2], rect[1], x, y)
            if tempPoint < nearestPoint:
                nearestPoint = tempPoint
                nearestRectangle=rect

            tempPoint = euclidian_distance(rect[0], rect[1]+rect[3], x, y)
            if tempPoint < nearestPoint:
                nearestPoint = tempPoint
                nearestRectangle=rect

            tempPoint = euclidian_distance(rect[0]+rect[2], rect[1]+rect[3], x, y)
            if tempPoint < nearestPoint:
                nearestPoint = tempPoint
                nearestRectangle=rect

        x,y,w,h = nearestRectangle
        cv2.rectangle(displayImage,(x,y),(x+w, y+h),(0,255,0), 3)
        cv2.imshow("ContourImage",displayImage)

cv2.namedWindow("ContourImage")
cv2.setMouseCallback("ContourImage", click_and_crop)

while True:
    cv2.imshow('ContourImage', displayImage)
    key = cv2.waitKey(1)
    
    if key == ord("c"):
        break

cv2.destroyAllWindows()