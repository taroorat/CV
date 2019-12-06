import cv2
import numpy as np
import os

for image in os.listdir('resimgs/'):
    img = cv2.imread('resimgs/'+image)
    bg1 = cv2.imread('images/bg/bg1/'+image)
    bg2 = cv2.imread('images/bg/bg2/'+image)
    h, w = img.shape[:2]
    print(h, w)
    for i in range(int(h)):
        for j in range(int(w)):
            if img[i, j][0] > 100 and img[i, j][1] > 100 and img[i, j][2] > 100 :
                img[i,j][0]=bg2[i,j][0]
                img[i, j][1] = bg2[i, j][1]
                img[i, j][2] = bg2[i, j][2]
            else:
                img[i,j][0]=bg1[i,j][0]
                img[i, j][1] = bg1[i, j][1]
                img[i, j][2] = bg1[i, j][2]

    cv2.imwrite('images/outputs/dance/'+image, img)
    # print(img)
