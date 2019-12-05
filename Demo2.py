import cv2
import numpy as np
import random
import os

srcDir='images/dp_semq/dajiwu/'

# for path in os.listdir(srcDir):
image = cv2.imread('images/dp_semq/dajiwu/000152.png')
h, w = image.shape[:2]

gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
print(ret)
cv2.imwrite('out.png', binary)
