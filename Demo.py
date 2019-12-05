import cv2
import numpy as np
import random
import os

for path in os.listdir('images/keypoint/dajiwu/'):
    image = cv2.imread('images/keypoint/dajiwu/'+path)
    h, w = image.shape[:2]
    line_img = np.zeros((h, w,3), dtype=np.uint8)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaus = cv2.GaussianBlur(gray, (3, 3), 0)
    gray_img = cv2.Canny(gaus, 50, 150, apertureSize=3)

    minLineLength = 5
    maxLineGap = 1
    lines = cv2.HoughLinesP(gray_img,1,np.pi/180,10,minLineLength,maxLineGap)
    print(len(lines))
    print(lines)
    for i in range(len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            cv2.line(line_img,(x1,y1),(x2,y2),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),30)
    cv2.imwrite('images/outputs/dajiwu/'+path,line_img)

