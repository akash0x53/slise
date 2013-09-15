from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf
import os

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
        #drawing area
        
        self.area=builder.get_object('preview')
        self.area.realize()
        self.area.connect('draw',self.onExpose)
                
        window.show_all()
        
    def onExpose(self,area,context):
               
        if self.path is not None:
                                   
            pix=GdkPixbuf.Pixbuf()
            img=pix.new_from_file(self.path)
                                    
            gdk.cairo_set_source_pixbuf(context,img,0,0)
            
            context.fill()
            context.paint()
            
                       
                                   
        
    def onSelectFile(self,event):
        self.path=event.get_filename()
        print self.path
        self.area.queue_draw()
        
    @property    
    def select_file(self):
        return self.path
                
    def onExit(self,event,data):
        print 'Bye...',event,data
        gtk.main_quit()
                    

if __name__=="__main__":
    a=Slise_win()
    gtk.main()
    
        
        

    
    