import cv2
import numpy as np
import random
import os

for path in os.listdir('images/keypoint/aa/'):
    image = cv2.imread('images/keypoint/aa/'+path)
    h, w = image.shape[:2]
    gray_img = np.zeros((h, w), dtype=np.uint8)
    line_img = np.zeros((h, w,3), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            if image[i,j][0]>0 or image[i,j][1] >0 or image[i,j][2] >0:
                gray_img[i,j]=255

    # cv2.imwrite('gray.jpg',gray_img)

    minLineLength = 5
    maxLineGap = 1
    lines = cv2.HoughLinesP(gray_img,1,np.pi/180,10,minLineLength,maxLineGap)
    print(len(lines))
    print(lines)
    for i in range(len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            cv2.line(line_img,(x1,y1),(x2,y2),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),30)
    cv2.imwrite('images/outputs/aa/'+path,line_img)

