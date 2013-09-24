# Adjust provided image with variety of parameters
# 1] if image size > 640x480, resize to 640x480
# 2] accept only color image (current support)
import cv2
from slise.slise_exception import SliseException 

class Adjust(object):
    def __init__(self):
        self.template=None
        
    @property                   
    def image(self):
        return self.template

    @image.setter
    def image(self,img):
        if img.shape[2]!=3 or img.dtype!='uint8' or (img.shape[1]<640 or img.shape[1]<480):
            raise SliseException("Image dimension error")
        else:
            print 'image set'
            self.template=img
    
    def resize(self):
        self.resized=cv2.resize(self.template,(640,480))
            
    def tohsv(self,img):
        self.hsv=cv2.cvtColor(img,cv2.cv.CV_BGR2HSV)
        
    
    @property
    def size(self):
        resoltion=str(self.template.shape[1])+"x"+str(self.template.shape[0])
        return resoltion
    