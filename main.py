from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf
from slise import __IMAGE_PATH__, __HISTOGRAM__
from slise.Adjust import Adjust
from slise.Features import Histogram
from slise.enumerate import EnumerateFiles
import thread
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
        select_file.set_name('file')
        select_file.connect('file-set',self.onSelectFile) #on selection of file using FileChooseDialog box it generates "file-set" signal
        #select_folder
        folder=builder.get_object('select_folder')
        folder.connect('file-set',self.onSelectFile)
        folder.set_name('folder')
        
        #image preview
        self.area=builder.get_object('preview')
        self.area.connect('draw',self.onExpose)
        #show histogram
        self.histogram=builder.get_object('histogram_canvas')
        self.histogram.connect_after('draw',self.drawHistogram)
        
        #FOR TEST
        icon_view=builder.get_object('result_view')
        liststore=builder.get_object('icon_list')
        icon_view.set_model(liststore)
        icon_view.set_pixbuf_column(0)
        icon_view.set_text_column(1)
        
        icon_view.set_name('view')
        self.area.set_name('da')
        #add CSS
        style=gtk.CssProvider()
        style.load_from_path('./gui/style.css')
        gtk.StyleContext.add_provider_for_screen(gdk.Screen.get_default(),style,gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
                        
        window.show_all()
            
    def onExpose(self,area,context):
        global __IMAGE_PATH__
        global __HISTOGRAM__    
        
        if __IMAGE_PATH__ is not None:
            pix=GdkPixbuf.Pixbuf()
            #print __IMAGE_PATH__
            img=pix.new_from_file_at_scale(__IMAGE_PATH__,300,300,1)
            gdk.cairo_set_source_pixbuf(context,img,0,0)
            context.fill()
            context.paint()
            
        if __HISTOGRAM__ is None and __IMAGE_PATH__ is not None :
            adjust_image=Adjust()
            adjust_image.image=cv2.imread(__IMAGE_PATH__)
            hist_calc=Histogram(adjust_image.image)
            hist_calc.get_histogram()
            __HISTOGRAM__=hist_calc.draw_histogram()
            #print __HISTOGRAM__
            self.histogram.queue_draw()
            
    def drawHistogram(self,area,context):
        global __HISTOGRAM__
        if __HISTOGRAM__ is not None:
            pix=GdkPixbuf.Pixbuf()
            img=pix.new_from_data(__HISTOGRAM__.tostring(),GdkPixbuf.Colorspace.RGB,False,8,__HISTOGRAM__.shape[1],__HISTOGRAM__.shape[0],__HISTOGRAM__.shape[1]*3,None,None)
            gdk.cairo_set_source_pixbuf(context,img,0,0)
            
            context.fill()
            context.paint()
            __HISTOGRAM__=None
        
    def onSelectFile(self,widget):
        global __IMAGE_PATH__
        global __FOLDER_PATH__
        
        print widget.get_name()         
        if widget.get_name()=="file":
            self.path=widget.get_filename()
            __IMAGE_PATH__=self.path
            self.area.queue_draw()
            
        elif widget.get_name()=="folder":
            __FOLDER_PATH__=widget.get_filename()
            self.gather_files(__FOLDER_PATH__)
            
    def gather_files(self,path):
        try:
            e=EnumerateFiles(path)
            e.start()
            e.join()
                                    
            print 'thread created',e.get_files
        except Exception as e:
            print 'Unable to start enumeration thread',e
               
                    
    def onExit(self,event,data):
        print 'Bye...',event,data
        gtk.main_quit()
                    

if __name__=="__main__":
    a=Slise_win()
    gtk.main()