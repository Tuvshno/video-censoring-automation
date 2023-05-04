import cv2 as cv
import numpy as np
from time import time
from windowCapture import WindowCapture

# wincap = WindowCapture('Adobe Premiere Pro 2023 - D:\\test_1.prproj')
wincap = WindowCapture('Adobe Premiere Pro 2023 - D:\\test_1.prproj')

loop_time = time()
while True:
    
    screenshot = wincap.get_screenshot()
    
    cv.imshow('Computer Vision', screenshot)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #wait 1 ms or quit with q
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
    
print('Done')