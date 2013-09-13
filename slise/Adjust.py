# Adjust provided image with variety of parameters
# 1] if image size > 640x480, resize to 640x480
# 2] accept only color image (current support)
import cv2
import numpy as np
from slise.slise_exception import SliseException 

class Adjust:
    def __init__(self,image):
        self.image=image
        if image is None:
            raise SliseException("No image provided")
            print 'Error: Image not found. Please provide image'
        
        if image.shape[2] is not 3:
            print 'image with 3 channel is supported'
    
    def resize(self):
        self.image=cv2.resize(self.image,(640,480))
        return self.image
    
    def tohsv(self):
        return cv2.cvtColor(self.image,cv2.cv.CV_BGR2HSV)
    
    
        
    @property
    def size(self):
        resoltion=str(self.image.shape[1])+"x"+str(self.image.shape[0])
        return resoltion
    