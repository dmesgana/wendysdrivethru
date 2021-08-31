import cv2
import numpy as np

im1 = cv2.imread('lemur.png')
im2 = cv2.imread('flag.png')

dest_xor = cv2.bitwise_xor(im1, im2, mask=None)

cv2.imshow('Bitwise XOR', dest_xor)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()