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

    def getFilenames(self):
        files = [self.mypath+"/"+f for f in listdir(self.mypath) if isfile(join(self.mypath, f)) and f.endswith(".bmp")]
        files.sort()
        print str(len(files))+" bmp files found."
        self.filenames = files

    def sum(self,count,gain):
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
        return self.normalise(sumimg,gain)
    
    def normalise(self,float64image,gain):
        m=np.max(float64image)
        float64image=np.around(float64image/m*255*gain)
        float64image=np.clip(float64image,0,255)
        return cv2.cvtColor(float64image.astype(np.uint8), cv2.COLOR_BGR2GRAY)

    
    def clahe(self,image,claheClipLimit):
        return cv2.createCLAHE(clipLimit=claheClipLimit).apply(image)
        
    def disp(self,image):
        cv2.imshow('Display',image)
        print "Press s to save, ESC to exit"
        while(True):
            k=cv2.waitKey(0)
            if k == 27:         # wait for ESC key to exit
                cv2.destroyAllWindows()
                break
            elif k == ord('s'): # wait for 's' key to save and exit
                cv2.imwrite("../twi/sample/saved.png",image)
                print "Saved"
                cv2.destroyAllWindows()    
                break;
            elif k == ord('h'):
                self.histo(image)

    def histo(self,image):
        plt.hist(image.ravel(),256,[0,256],color='r')
        plt.xlim([0,256])
        plt.show()


if __name__ == '__main__':
    imSet=imageSet(sys.argv[1])
    sumImage=imSet.sum(0,1)
    claheImage=imSet.clahe(sumImage,5)
    imSet.disp(claheImage)
