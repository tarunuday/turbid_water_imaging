#!/usr/bin/env python                                                                                             

import numpy as np
import sys
from std_msgs.msg import String
import cv2
import json

class moveStripe:
    
    def __init__(self):
        windowName="Display"
        screen_size_x = 1080
        screen_size_y = 1920

        #  -------------> y (cols)
        #
        # |
        # |
        # V
        #
        # x
        # (rows)

        projection_ratio_x = 1
        projection_ratio_y = 0.75 
        image = np.zeros([screen_size_x, screen_size_y], dtype=np.uint8)
        color = (255,255,255)        

        block_start_x=(int)(screen_size_x*(1-projection_ratio_x)/2)
        block_start_y=(int)(screen_size_y*(1-projection_ratio_y)/2)
        
        n_x=20
        n_y=1

        block_x=block_start_x
        block_y=block_start_y

        block_len_x=screen_size_x/n_x
        block_len_y=(int)(screen_size_y*projection_ratio_y)
        
        overlap= 0.9

        cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
        cv2.imshow(windowName,image)
        cv2.moveWindow(windowName,1920,0)
        cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        
        print("Press arrow keys/space to move, ESC to exit \n")

        print("Block Position: Floodlight ")    
        positions=screen_size_x*projection_ratio_x//(overlap*block_len_x)
        image = np.zeros([screen_size_x,screen_size_y], dtype=np.uint8)
        cv2.rectangle(image,(block_y,block_x),(block_y+(int)(screen_size_y*projection_ratio_y),block_x+(int)(screen_size_x*projection_ratio_x)),color,-1)
        cv2.imshow(windowName,image)
        while(True):
            k=cv2.waitKey(0)
            if k == 27:         # wait for ESC key to exit
                cv2.destroyWindow(windowName)
                break
            elif k == 84 or k == 32:
                block_number=1
                while(True):
                    sys.stdout.write("\033[F")
                    print("Block Position: "+str(block_number)+"/"+str(int(positions))+"                        ")
                    
                    image = np.zeros([screen_size_x,screen_size_y], dtype=np.uint8)
                    cv2.rectangle(image,(block_y,block_x),(block_y+block_len_y,block_x+block_len_x),color,-1)
                    cv2.imshow(windowName,image)
                    k=cv2.waitKey(0)
                    
                    if k == 27:         # wait for ESC key to exit
                        cv2.destroyWindow(windowName)
                        break
                    elif k == 84 or k == 32:
#                        if(block_x+block_len_x<screen_size_x*projection_ratio_x):
                        if(block_number<positions):
                            block_x=block_x+int(overlap*block_len_x)
                            block_number+=1
                        else:
                            block_number=1
                            block_x=block_start_x
                    else:
                        print(k)
                break
            
if __name__ == '__main__':
    ms=moveStripe()
