import cv2
import numpy as np
import os
import sys

path = sys.argv[1]
cap = cv2.VideoCapture(0)
img = cv2.imread(rf'{path}',cv2.IMREAD_COLOR)
imgContour = img.copy()

def empty(a):
    pass

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(len(contours))
    areaMin = cv2.getTrackbarPos("min_area", "Parameters")
    print('areaMin:',areaMin,type(areaMin))
    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("min_area", "Parameters")

        if area > areaMin:

            count += 1

            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 1)
        else:
            None


    print('count:',count)
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("threshold_min","Parameters",23,255,empty)
cv2.createTrackbar("threshold_max","Parameters",20,255,empty)
cv2.createTrackbar("min_area","Parameters",200,220,empty)

while True:
    imgContour = img.copy()
    th1 = cv2.getTrackbarPos("threshold_min", "Parameters")
    th2 = cv2.getTrackbarPos("threshold_max", "Parameters")
    area = cv2.getTrackbarPos("min_area","Parameters")

    _, frame = cap.read()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (15,15), 0)
    kernel2 = np.ones((15,15), np.float32) /225
    blur_two = cv2.filter2D(gray_image,-1,kernel2)
    median_blur = cv2.medianBlur(gray_image,5)
    ret, thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # median_blur or gray_image can be applied for this
    img_canny = cv2.Canny(median_blur,th1,th2)
    # img_canny = cv2.Canny(gray_image, th1, th2)
    getContours(thresh,imgContour)





    cv2.imshow('gray',gray_image)
    #thresh is best so far
    cv2.imshow('thresh',thresh)
    cv2.imshow('contour',imgContour)
    cv2.waitKey(500)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()