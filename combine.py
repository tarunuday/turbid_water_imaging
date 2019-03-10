#!/usr/bin/env python                                                                                              

import numpy as np
import sys
from  matplotlib import pyplot as plt
from std_msgs.msg import String
from os import listdir
from os.path import isfile, join
import cv2
import time

class imageSet:
    
    def __init__(self,mypath,imageFormat):
        if(mypath[-1] is '/'):
            mypath=mypath[0:-1]
        self.mypath=mypath
        self.imageFormat=imageFormat
        self.path=mypath.split('/')
        self.saveFileName=str(self.path[-2])+"_"+str(self.path[-1])
        self.getFilenames(self.imageFormat)
        self.count=len(self.filenames)
        self.displaysOn=0

    def getFilenames(self,imageFormat):
        files = [self.mypath+"/"+f for f in listdir(self.mypath) if isfile(join(self.mypath, f)) and f.endswith(imageFormat)]
        files.sort()
        print str(len(files))+" "+imageFormat+" files found.\n"
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
  
    def normalise(self,float64image):
        m=np.max(float64image)
        float64image=np.around(float64image/m*255)
        float64image=np.clip(float64image,0,255)
        return float64image.astype(np.uint8)
    
    def applyclahe(self,image,claheClipLimit,tileDim):
        try:
            image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except:
            pass
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
                cv2.imwrite("/home/tarun/projects/thesis/samples/"+self.saveFileName+".png",image)
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

    def maxpix(self,nimages):
        try:
            self.filenames
        except NameError:
            self.getFilenames(self.imageFormat)
        
        lfn=len(self.filenames)
                
        if nimages is 0:
            count=lfn
        elif nimages > lfn:
            print("Requested to sum "+str(nimages)+" files. Only "+str(lfn)+" files exist.\n")
            count=lfn
        else:
            count=nimages
        
        maxpiximg=cv2.imread(self.filenames[0])
        maxpiximg=cv2.cvtColor(maxpiximg, cv2.COLOR_BGR2GRAY)
        rimg=(maxpiximg.shape)[0]
        cimg=(maxpiximg.shape)[1]
        for i in range(count):
            sys.stdout.write("\033[F")
            print "Maxpixing image "+str(i+1)+" out of "+str(count)
            img=cv2.imread(self.filenames[i])
            img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            for x in range(rimg):
                for y in range(cimg):
                    if maxpiximg[x,y]<img[x,y]:
                        maxpiximg[x,y]=img[x,y]
        return maxpiximg   

if __name__ == '__main__':
    args=len(sys.argv)
    if args == 1:
        print("Error: Enter directory")
        quit()
    if args >= 2:
        directory=sys.argv[1]
    if args >= 3:
        noimages=sys.argv[2]
    else:
        noimages=0
    if args >= 4:
        imageFormat=sys.argv[3]
    else:
        imageFormat=".JPG"

    imSet=imageSet(directory,imageFormat)
    if len(imSet.filenames) is 0:
        print("Error: No files found")
        quit()
    image=imSet.maxpix(int(noimages))
    imSet.disp(image)
    
