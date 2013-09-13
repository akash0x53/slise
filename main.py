import cv2
from slise.Adjust import Adjust
from slise.slise_exception import SliseException
from slise.Features import Histogram

if __name__=="__main__":
    img=cv2.imread('temp.jpg')
    
    cam=cv2.VideoCapture()
    cam.open(-1)
    
    
    while True:
        _,frm=cam.read()
        
        obj=Adjust(frm)
        obj.resize()
        
        hist=Histogram(obj.tohsv())
        hist.get_histogram()
        
        cv2.imshow("histo",hist.draw_histogram())
        cv2.imshow("video",frm)
        
        if cv2.waitKey(5)>10:
            break
        
        