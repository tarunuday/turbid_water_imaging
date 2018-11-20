#!/usr/bin/env python                                                                                             

import numpy as np
import sys
from  matplotlib import pyplot as plt
from std_msgs.msg import String
from os import listdir
from os.path import isfile, join
import cv2
import time
import json

class imageSet:
    
    def __init__(self,mypath):
        if(mypath[-1] is '/'):
            mypath=mypath[0:-1]
        self.mypath=mypath
        self.directory=mypath.split('/')[-1]
        self.getFilenames()
        self.count=len(self.filenames)
        self.displaysOn=0
        self.imageFormat=".JPG"

    def getFilenames(self):
        files = [self.mypath+"/"+f for f in listdir(self.mypath) if isfile(join(self.mypath, f)) and f.endswith(".JPG")]
        files.sort()
        print str(len(files))+"  files found.\n"
        self.filenames = files

    def sum(self,count):
        try:
            self.filenames
        except NameError:
            self.getFilenames()

        if count==0:
            count=len(self.filenames)
        elif count>len(self.filenames):
            print "Requested to sum "+str(count)+" files. Only "+str(len(self.filenames))+" files exist."
            count=len(self.filenames)

        im=cv2.imread(self.filenames[0])
        sumimg=np.float64(im-im)
        for i in range(count):
            sys.stdout.write("\033[F")
            print "Summing image "+str(i+1)+" out of "+str(count)
            img=cv2.imread(self.filenames[i])
            sumimg+=np.float64(img)
        print ""
        img=self.normalise(sumimg)
        return img

    def normalise(self,float64image):
        m=np.max(float64image)
        float64image=np.around(float64image/m*255)
        float64image=np.clip(float64image,0,255)
        return float64image.astype(np.uint8)

    
    def applyclahe(self,image,claheClipLimit,tileDim):
        image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.createCLAHE(clipLimit=claheClipLimit,tileGridSize=(tileDim,tileDim)).apply(image)
        
    def disp(self,image):
        windowName="Display"+str(self.displaysOn)
        self.displaysOn+=1
        cv2.namedWindow(windowName,cv2.WINDOW_NORMAL)
        cv2.imshow(windowName,image)
        cv2.resizeWindow(windowName, 1000,1000)
        print "Press s to save, ESC to exit"
        while(True):
            k=cv2.waitKey(0)
            if k == 27:         # wait for ESC key to exit
                cv2.destroyWindow(windowName)
                self.displaysOn-=1
                break
            elif k == ord('s'): # wait for 's' key to save and exit
                cv2.imwrite("/home/tarun/projects/thesis/samples/"+str(int(time.mktime(time.gmtime())))+".png",image)
                print "Saved"
                self.displaysOn-=1
                cv2.destroyWindow(windowName)
                break;
            elif k == ord('h'):
                self.histo(image)

    def histo(self,image):
        plt.hist(image.ravel(),256,[0,256],color='r')
        plt.xlim([0,256])
        plt.show()

    def clahesum(self,count,clipLimit,tileDim):
        try:
            self.filenames
        except NameError:
            self.getFilenames()

        if count==0:
            count=len(self.filenames)
        elif count>len(self.filenames):
            print "Requested to sum "+str(count)+" files. Only "+str(len(self.filenames))+" files exist. \n"
            count=len(self.filenames)

        image=cv2.imread(self.filenames[0])
        image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sumimg=np.float64(image-image)
        for i in range(count):
            sys.stdout.write("\033[F")
            print "Applying clahe and summimg image "+str(i+1)+" out of "+str(count)
            img=cv2.imread(self.filenames[i])
            img=self.applyclahe(img,clipLimit,tileDim)
            sumimg+=np.float64(img)
        print ""
        img=self.normalise(sumimg)
        return img

if __name__ == '__main__':
    args=len(sys.argv)
    if args == 1:
        print("Enter directory")
    if args >= 2:
        imSet=imageSet(sys.argv[1])
    if args >= 3:
        noimages=sys.argv[2]
    else:
        noimages=22
    image=imSet.applyclahe(imSet.sum(noimages),8,8)
#    image=imSet.clahesum(noimages,8,8)
#    image=imSet.sum(noimages)
    imSet.disp(image)
