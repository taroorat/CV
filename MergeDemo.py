import cv2
import numpy as np

img = cv2.imread('images/bg/out.png')
bg1= cv2.imread('images/bg/bg1.PNG')
bg2 = cv2.imread('images/bg/bg2.PNG')
h, w = img.shape[:2]
print(h,w)
for i in range(int(h/2)):
    for j in range(int(w/2)):
        if img[i, j][0] > 0 :
            img[i,j][0]=bg1[i,j][0]
            img[i, j][1] = bg1[i, j][1]
            img[i, j][2] = bg1[i, j][2]
        else:
            img[i,j][0]=bg2[i,j][0]
            img[i, j][1] = bg2[i, j][1]
            img[i, j][2] = bg2[i, j][2]

cv2.imwrite('out.png', img)
# print(img)
