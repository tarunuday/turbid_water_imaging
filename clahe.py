#!/usr/bin/env python                                                                                              

import numpy as np
import sys
from  matplotlib import pyplot as plt
from std_msgs.msg import String
from os import listdir
from os.path import isfile, join
import cv2
import time

pt_tl=(300,300)
pt_br=(3000,1500)



def applyclahe(image,claheClipLimit,tileDim):
    try:
        image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        pass
    return cv2.createCLAHE(clipLimit=claheClipLimit,tileGridSize=(tileDim,tileDim)).apply(image)

def Qscore(image):
    image=image[pt_tl[1]:pt_br[1],pt_tl[0]:pt_br[0]]
    sharpness = cv2.Laplacian(image, cv2.CV_64F).var()
    contrast = np.log(-1* cv2.Laplacian(image, cv2.CV_64F).mean())
#    snr=10*np.log(np.mean(image)/np.std(image))
    print("Blur score: "+str(sharpness))
    print("Contrast score: "+str(contrast))
#    print("SNR: "+str(snr))

def disp(image,name):
    windowName="Display"
    cv2.namedWindow(windowName,cv2.WINDOW_NORMAL)
    cv2.imshow(windowName,image)
    cv2.resizeWindow(windowName, 1500,1500)
    print "Press s to save, ESC to exit"
    while(True):
        k=cv2.waitKey(0)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyWindow(windowName)
            break
        elif k == ord('s'): # wait for 's' key to save and exit
            t=str(int(time.mktime(time.gmtime())))
            cv2.imwrite("/home/tarun/projects/thesis/samples/"+name+"_fl"+".png",image)
            print "Saved"
            cv2.destroyWindow(windowName)
            break;
        elif k == ord('h'):
            histo(image)

def histo(image):
    plt.hist(image.ravel(),256,[0,256],color='r')
    plt.xlim([0,256])
    plt.show()

if __name__ == '__main__':
    args=len(sys.argv)
    if args == 1:
        print("Error: Enter image")
        quit()
    if args >= 2:
        im=sys.argv[1]
    if args >= 3:
        claheLim=float(sys.argv[2])
    else:
        claheLim=2
    if args >= 4:
        tileDim=int(sys.argv[3])
    else:
        tileDim=8

    image=cv2.imread(im)
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    disp(image,im.split('/')[-3])
        
