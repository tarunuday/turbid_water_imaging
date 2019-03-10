#!/usr/bin/env python                                                                                             

import numpy as np
import sys
from std_msgs.msg import String
import cv2
import time

class moveStripe:
    
    def logwriter(self):
        f=open("logs/lighting.txt","a")
        if time.localtime().tm_hour<10:
            time_hour="0"+str(time.localtime().tm_hour)
        else:
            time_hour=str(time.localtime().tm_hour)
        if time.localtime().tm_min<10:
            time_min="0"+str(time.localtime().tm_min)
        else:
            time_min=str(time.localtime().tm_min)
        if time.localtime().tm_sec<10:
            time_sec="0"+str(time.localtime().tm_sec)
        else:
            time_sec=str(time.localtime().tm_sec)
        f.write("date: "+str(time.localtime().tm_year)+"/"+str(time.localtime().tm_mon)+"/"+ str(time.localtime().tm_mday)+" ")
        f.write(" time: "+str(time_hour)+":"+str(time_min)+":"+ str(time_sec))
        f.write(" blockdim (#x #y ovrlap): ("+str(self.no_of_blocks_x)+" "+str(self.no_of_blocks_y)+" "+str(self.overlap)+")")
        f.write(" cur pos (x y): ("+str(self.cur_pos_x)+" "+str(self.cur_pos_y)+")")
        f.write(" max pos (x y): ("+str(self.max_pos_x)+" "+str(self.max_pos_y)+")")
        f.write("\n")
        f.close()

    def __init__(self):
        windowName="Display"
        self.screen_size_x = 1080
        self.screen_size_y = 1920
        self.no_of_blocks_x=5
        self.no_of_blocks_y=5
        self.overlap= 0.3

        #  -------------> y (cols)
        #
        # |
        # |
        # V
        #
        # x
        # (rows)

        projection_ratio_x = 0.75
        projection_ratio_y = 0.75 
        image = np.zeros([self.screen_size_x, self.screen_size_y], dtype=np.uint8)
        color = (255,255,255)        

        block_start_x=(int)(0)#self.screen_size_x*(1-projection_ratio_x)/2)
        block_start_y=(int)(self.screen_size_y*(1-projection_ratio_y)/2)
        
        block_x=block_start_x
        block_y=block_start_y

        block_len_x=(int)(self.screen_size_x*projection_ratio_x/self.no_of_blocks_x)
        block_len_y=(int)(self.screen_size_y*projection_ratio_y/self.no_of_blocks_y)

        self.max_pos_x=(int)(self.screen_size_x*projection_ratio_x//((1-self.overlap)*block_len_x))
        self.max_pos_y=(int)(self.screen_size_y*projection_ratio_y//((1-self.overlap)*block_len_y))

        cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
        cv2.imshow(windowName,image)
        cv2.moveWindow(windowName,1920,0)
        cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

        self.cur_pos_x=-1;
        self.cur_pos_y=-1;
        self.logwriter()
        cv2.waitKey(0)
        print("Press arrow keys/space to move, ESC to exit \n")

        self.cur_pos_x=0;
        self.cur_pos_y=0;
        self.logwriter()
        print("Block Position: Floodlight ")    
        image = np.zeros([self.screen_size_x,self.screen_size_y], dtype=np.uint8)
        cv2.rectangle(image,(block_y,block_x),(block_y+(int)(self.screen_size_y*projection_ratio_y),block_x+(int)(self.screen_size_x*projection_ratio_x)),color,-1)
        cv2.imshow(windowName,image)

#        while(True):
        k=cv2.waitKey(0)
        #    if k == 27:         # wait for ESC key to exit
         #       cv2.destroyWindow(windowName)
         #       break
         #   elif k == 84 or k == 32:
        self.cur_pos_x=1
        self.cur_pos_y=1
        while(True):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            self.logwriter()
            print("Block Position x: "+str(self.cur_pos_x)+"/"+str(int(self.max_pos_x))+"                        ")
            print("Block Position y: "+str(self.cur_pos_y)+"/"+str(int(self.max_pos_y))+"                        ")
            
            image = np.zeros([self.screen_size_x,self.screen_size_y], dtype=np.uint8)
            
            block_y=block_start_y+(self.cur_pos_y-1)*int((1-self.overlap)*block_len_y)
            block_x=block_start_x+(self.cur_pos_x-1)*int((1-self.overlap)*block_len_x)

            cv2.rectangle(image,(block_y,block_x),(block_y+block_len_y,block_x+block_len_x),color,-1)
            cv2.imshow(windowName,image)
            k=cv2.waitKey(0)
            
            if k == 27:         # wait for ESC key to exit
                cv2.destroyWindow(windowName)
                break
            elif k == 84 or k == 32:
                if(self.cur_pos_y<self.max_pos_y):
                    self.cur_pos_y+=1
                else:
                    self.cur_pos_y=1
                    if(self.cur_pos_x<self.max_pos_x):
                        self.cur_pos_x+=1 
                    else:
                        self.cur_pos_x=1
            else:
                print(k)
        
if __name__ == '__main__':
    ms=moveStripe()
