#!/usr/bin/env python

import numpy as np
import sys
from  matplotlib import pyplot as plt
from std_msgs.msg import String
from os import listdir
from os.path import isfile, join
import cv2

claheClipLimit=4
tileDim=8

fl = cv2.imread("../samples/1543461432_st450ms60px.png")
fl=cv2.cvtColor(fl, cv2.COLOR_BGR2GRAY)
print(fl.shape)
fl=fl[1000:5000,0:4000]
fl= cv2.createCLAHE(clipLimit=claheClipLimit,tileGridSize=(tileDim,tileDim)).apply(fl)
cv2.imwrite("../samples/fl.png",fl)

st = cv2.imread("../samples/full_striped.png")
st=cv2.cvtColor(st, cv2.COLOR_BGR2GRAY)
st=st[1000:5000,000:5000]
st= cv2.createCLAHE(clipLimit=claheClipLimit,tileGridSize=(tileDim,tileDim)).apply(st)
cv2.imwrite("../samples/st.png",st)


windowName="w1"
cv2.namedWindow(windowName,cv2.WINDOW_NORMAL)
cv2.imshow(windowName,fl)

cv2.resizeWindow(windowName, 1000,1000)
cv2.waitKey(0)

windowName="w2"
cv2.namedWindow(windowName,cv2.WINDOW_NORMAL)
cv2.imshow(windowName,st)
cv2.resizeWindow(windowName, 1000,1000)
cv2.waitKey(0)
