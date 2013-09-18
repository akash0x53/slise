import os
from slise import __FOLDER_PATH__
from threading import Thread

class EnumerateFiles(Thread):
    
    def __init__(self,path):
        Thread.__init__(self)
        self.path=path
        
    def run(self):
        self.enumerate()
        
    def enumerate(self):
        global __FOLDER_PATH__
        print 'function called'
        
        self.files=temp=list()
        
        for (_,_,filename) in os.walk(self.path):
            temp.extend(filename)
        
        for single_file in temp:
            _,ext=os.path.splitext(single_file)
            
            if ext.lower() in ('.jpg','.jpeg','.png'):
                self.files.append(single_file)
            
                
            
    @property
    def get_files(self):
        return self.files
    
                
        
        
    
        