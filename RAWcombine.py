#!/usr/bin/env python                                                                                             

import cv2
import numpy as np
fd = open('/home/tarun/projects/thesis/Nov032018/raw/DSC00020.ARW', 'rb')
f = np.fromfile('/home/tarun/projects/thesis/Nov032018/raw/DSC00020.ARW', dtype=np.uint8)
f=list(f)
print(str(len(f)/24))
#im = f.reshape((1000,1000,3)) #notice row, column format
#fd.close()
#This makes a numpy array that can be directly manipulated by OpenCV

#cv2.imshow('', im)
#cv2.waitKey()
#cv2.destroyAllWindows()
