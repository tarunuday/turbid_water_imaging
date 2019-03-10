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
#        self.saveFileName=str(self.path[-2])+"_"+str(self.path[-1])
        self.getFilenames(self.imageFormat)
        self.count=len(self.filenames)

        self.pt_tl=(1500,300)
        self.pt_br=(3000,1500)
        self.sig_tl=(2600,450)
        self.sig_br=(2900,750)
        self.sig2_tl=(2500,1700)
        self.sig2_br=(2800,2000)
        self.bg_tl=(3100,2800)
        self.bg_br=(3400,3100)
        #self.Qscore()
        self.slicer()

    def getFilenames(self,imageFormat):
        files = [self.mypath+"/"+f for f in listdir(self.mypath) if isfile(join(self.mypath, f)) and f.endswith(imageFormat)]
        files.sort()
        print str(len(files))+" "+imageFormat+" files found.\n"
        self.filenames = files
    
    def applyclahe(self,image,claheClipLimit,tileDim):
        try:
            image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except:
            pass
        return cv2.createCLAHE(clipLimit=claheClipLimit,tileGridSize=(tileDim,tileDim)).apply(image)

    def Qscore(self):
        for i in range(self.count):
            origimage=cv2.imread(self.filenames[i])
            image=origimage[1500:5000,300:3900]
            snr_sig=image[self.sig_tl[1]:self.sig_br[1],self.sig_tl[0]:self.sig_br[0]]
            snr_sig2=image[self.sig2_tl[1]:self.sig2_br[1],self.sig2_tl[0]:self.sig2_br[0]]
            snr_bg=image[self.bg_tl[1]:self.bg_br[1],self.bg_tl[0]:self.bg_br[0]]
            blurimg=image[self.pt_tl[1]:self.pt_br[1],self.pt_tl[0]:self.pt_br[0]]
            
            #if i is 1:
            #    self.disp(blurimg,"example")
            sharpness = cv2.Laplacian(blurimg, cv2.CV_64F).var()
            #contrast=np.log(np.mean(snr_sig)/np.mean(snr_bg))
            contrast=np.log(np.mean(snr_sig2)/np.mean(snr_bg))
            print("\n"+(self.filenames[i]).split('/')[-1]+"\t"+str(sharpness)+"\t"+str(contrast))         
            
    def slicer(self):
        for i in range(self.count):
            origimage=cv2.imread(self.filenames[i])
            image=origimage[1500:5000,300:3900]
            snr_sig=image[self.sig_tl[1]:self.sig_br[1],self.sig_tl[0]:self.sig_br[0]]
            cv2.imwrite("/home/tarun/projects/thesis/samples/supersliced/"+str(self.filenames[i].split('/')[-1])[0:-4]+"_sliced.png",snr_sig)
                
    def disp(self,image,name):
        windowName="Display"
        cv2.namedWindow(windowName,cv2.WINDOW_NORMAL)
        cv2.rectangle(image,self.pt_tl,self.pt_br,10,4)
        cv2.rectangle(image,self.sig_tl,self.sig_br,200,8)
        cv2.rectangle(image,self.bg_tl,self.bg_br,800,8)
        cv2.imshow(windowName,image)
        cv2.resizeWindow(windowName, 1000,1000)
        print "Press s to save, ESC to exit"
        while(True):
            k=cv2.waitKey(0)
            if k == 27:         # wait for ESC key to exit
                cv2.destroyWindow(windowName)
                break
            elif k == ord('s'): # wait for 's' key to save and exit
                cv2.imwrite("/home/tarun/projects/thesis/samples/sliced/"+name+"_sl.png",image)
                print "Saved"
                cv2.destroyWindow(windowName)
                break;
            elif k == ord('h'):
                self.histo(image)

    def histo(self,image):
        plt.hist(image.ravel(),256,[0,256],color='r')
        plt.xlim([0,256])
        plt.show()

if __name__ == '__main__':
    args=len(sys.argv)
    directory="../samples/maxpix/"
    imageFormat=".png"

    imSet=imageSet(directory,imageFormat)
    if len(imSet.filenames) is 0:
        print("Error: No files found")
    quit()
    
