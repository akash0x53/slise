import cv2
import numpy as np
from slise import __THRESH_VAL__

class Histogram:
    def __str__(self):
        return 'Class Histogram'
    
    def __init__(self,img):
        self.image=img
        
    def __eq__(self,another_histo):
        difference=cv2.compareHist(self.hist[0],another_histo.hist[0],cv2.cv.CV_COMP_CORREL)
        
        difference*=100
        if difference>=__THRESH_VAL__:
            return True
        return False
        
    
    def get_histogram(self):
        channels=self.image[:,:,0],self.image[:,:,1],self.image[:,:,2]
        self.hist=list()
        
        for i in range(0,len(channels)):
            #print i
            temp_histo=cv2.calcHist([channels[i]], [0], None,[256],[0,255])
            temp_histo=cv2.normalize(temp_histo,temp_histo,0,100,cv2.NORM_MINMAX)
            self.hist.append(temp_histo)
            #print temp_histo
        return self.hist
            
    def draw_histogram(self):
        canvas=np.zeros((300,256,3),'uint8')
        
        temp1=np.zeros((300,256,3),'uint8')
        temp2=np.zeros((300,256,3),'uint8')
        temp3=np.zeros((300,256,3),'uint8')
        
        x=0
        for pt in self.hist[2]:
            cv2.line(temp1, (x,100), (x,100-pt), (255,0,0))
            x+=1
       
        x=0
        for pt in self.hist[1]:
            cv2.line(temp2, (x,200), (x,200-pt), (0,255,0))
            x+=1
            
        x=0
        for pt in self.hist[0]:
            cv2.line(temp3, (x,300), (x,300-pt), (0,0,255))
            x+=1
                
        canvas=cv2.addWeighted(temp1,1.0, temp2, 1.0,0)
        canvas=cv2.addWeighted(canvas,1.0,temp3,1.0,0)               
        
                       
        return canvas    
            
            
            
        
        
        
        
        
        
     
