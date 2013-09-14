from gi.repository import Gtk as gtk
import os

class Slise_win:
    
    def __init__(self):
        ui_file=os.path.dirname(__file__)+"/gui/slise.glade"
        
        if os.path.exists(ui_file):
            print 'found glade...'
        
        builder=gtk.Builder()
        builder.add_from_file(ui_file)
        
        #main window
        window=gtk.Window()
        window=builder.get_object('window1')
        window.connect('delete-event',self.onExit)
        
        
        
        window.show_all()
        
    def onExit(self,event,data):
        print 'Bye...',event,data
        gtk.main_quit()
                    

if __name__=="__main__":
    a=Slise_win()
    gtk.main()
    
        
        

    
    