import numpy as np
import argparse
import imutils
import cv2


 
image = cv2.imread('288998637_5205692686212685_3121065976811889480_n.jpg')
cv2.imshow("Original", image)


rotated = imutils.rotate_bound(image, -45)
cv2.imshow("Rotated Without Cropping", rotated)
cv2.waitKey(0)


# M = cv2.getRotationMatrix2D(center, -90, 1.0)
# rotated = cv2.warpAffine(image, M, (w, h))
# cv2.imshow("Rotated by -90 Degrees", rotated)
