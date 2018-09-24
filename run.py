import cv2
import numpy as np

refPt = []

rawImage = cv2.imread("narrow_path_1.jpg")
blurImage = cv2.bilateralFilter(rawImage, 3, 75, 75)
grayImage = cv2.cvtColor(blurImage, cv2.COLOR_BGR2GRAY)
cannyImage = cv2.Canny(grayImage, 150, 250, 3)
# Overlap image and edges together
#tmp_img = np.bitwise_or(tmp_img, edges)
#tmp_img = cv2.addWeighted(tmp_img, 1 - edges_val, edges, edges_val, 0)

image, contours, hierachy = cv2.findContours(cannyImage, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contourImage = cv2.drawContours(rawImage, contours, -1, (0,255,0), 1)

def click_and_crop(event, x, y, flags, param):
    global refPt 
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]

# Straight Rectangle
candidateContour = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    height, width, channels = rawImage.shape
    if height/15 < h and width/15 < w:
        rawImage = cv2.rectangle(rawImage,(x,y),(x+w, y+h),(0,0,255), 1)
        candidateContour.append(cnt)

cv2.namedWindow("Contour image")
cv2.namedWindow("Raw image")
cv2.setMouseCallback("Contour image", click_and_crop)

while True:
    cv2.imshow('Contour image', contourImage)
    cv2.imshow('Raw image', rawImage)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("c"):
        break
    print(refPt)

cv2.destroyAllWindows()