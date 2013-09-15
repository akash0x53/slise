from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf
from slise import __IMAGE_PATH__, __HISTOGRAM__

import os,cv2

class Slise_win:
    
    def __init__(self):
        self.path=None
        ui_file=os.path.dirname(__file__)+"/gui/slise.glade"
        
        if os.path.exists(ui_file):
            print 'found glade...'
        
        builder=gtk.Builder()
        builder.add_from_file(ui_file)
        
        #main window
        window=gtk.Window()
        window=builder.get_object('window1')
        window.connect('delete-event',self.onExit)
        #file chooser dialog box
        select_file=builder.get_object('file_chooser')
        select_file.connect('file-set',self.onSelectFile) #on selection of file using FileChooseDialog box it generates "file-set" signal
        #image preview
        self.area=builder.get_object('preview')
        self.area.connect('draw',self.onExpose)
        #show histogram
        self.histogram=builder.get_object('histogram_canvas')
        self.histogram.connect('draw',self.drawHistogram) 
                        
        window.show_all()
        
    def onExpose(self,area,context):
        global __IMAGE_PATH__    
        if __IMAGE_PATH__ is not None:
            pix=GdkPixbuf.Pixbuf()
            print __IMAGE_PATH__
            img=pix.new_from_file_at_scale(__IMAGE_PATH__,300,300,1)
            gdk.cairo_set_source_pixbuf(context,img,0,0)
            context.fill()
            context.paint()
            
    def drawHistogram(self,arear,context):
        global __HISTOGRAM__
        
        if __HISTOGRAM__ is not None:
            pix=GdkPixbuf.Pixbuf()
            img=pix.new_from_data(__HISTOGRAM__.tostring(),GdkPixbuf.Colorspace.RGB,False,8,__HISTOGRAM__.shape[1],__HISTOGRAM__.shape[0],__HISTOGRAM__.strides[0],None,None)
            
            gdk.cairo_set_source_pixbuf(context,img,0,0)
            context.fill()
            context.paint()
                                   
        
    def onSelectFile(self,event):
        global __IMAGE_PATH__
        self.path=event.get_filename()
        __IMAGE_PATH__=self.path
        self.area.queue_draw()
        self.histogram.queue_draw()
        
                    
    def onExit(self,event,data):
        print 'Bye...',event,data
        gtk.main_quit()
        
    
                    

'''if __name__=="__main__":
    a=Slise_win()
    gtk.main()'''
    
        
        

    
    