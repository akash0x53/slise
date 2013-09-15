from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf
from slise import __IMAGE_PATH__, __HISTOGRAM__
from Adjust import Adjust
from Features import Histogram
import array

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
        self.histogram.connect_after('draw',self.drawHistogram) 
                        
        window.show_all()
        
    def onExpose(self,area,context):
        global __IMAGE_PATH__
        global __HISTOGRAM__    
        
        if __IMAGE_PATH__ is not None:
            pix=GdkPixbuf.Pixbuf()
            print __IMAGE_PATH__
            img=pix.new_from_file_at_scale(__IMAGE_PATH__,300,300,1)
            gdk.cairo_set_source_pixbuf(context,img,0,0)
            context.fill()
            context.paint()
            
        if __HISTOGRAM__ is None and __IMAGE_PATH__ is not None :
            print 'its none'
            adjust_image=Adjust()
            adjust_image.image=cv2.imread(__IMAGE_PATH__)
            hist_calc=Histogram(adjust_image.image)
            hist_calc.get_histogram()
            __HISTOGRAM__=hist_calc.draw_histogram()
            print __HISTOGRAM__
            self.histogram.queue_draw()
            
    def drawHistogram(self,arear,context):
        global __HISTOGRAM__
        global __IMAGE_PATH__
        
        if __HISTOGRAM__ is not None:
            print 'histo called'
            
            pix=GdkPixbuf.Pixbuf()
            print __HISTOGRAM__.shape
            print __HISTOGRAM__.dtype
                       
            
            img=pix.new_from_data(__HISTOGRAM__.tostring(),GdkPixbuf.Colorspace.RGB,False,8,256,300,256*3,None,None)
            
            gdk.cairo_set_source_pixbuf(context,img,0,0)
            
            context.fill()
            context.paint()
            __HISTOGRAM__=None
            
    def temp(self,event):
        print 'error',event
                                
        
    def onSelectFile(self,event):
        global __IMAGE_PATH__
        self.path=event.get_filename()
        __IMAGE_PATH__=self.path
        self.area.queue_draw()
        
        
                    
    def onExit(self,event,data):
        print 'Bye...',event,data
        gtk.main_quit()
        
    
                    

if __name__=="__main__":
    a=Slise_win()
    gtk.main()
    
        
        

    
    