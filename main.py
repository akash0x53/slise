#!/usr/bin/env python

#SLISE: Simple Local Image Search Engine 
#Author: Akash Shende
#contact: akash0x53s@gmail.com

#right now, it compares *only* __blue__ channel.

from multiprocessing.pool import ThreadPool
import os,cv2
import gi.repository.Gtk as gtk
import gi.repository.Gdk as gdk
from gi.repository import GdkPixbuf
from slise import __IMAGE_PATH__
from slise import __CURR_FILE__
from slise import __MATCHED_FILE__
from slise import __HISTOGRAM__
from slise import  __FILES__
from slise.Adjust import Adjust
from slise.Features import Histogram
from slise.slise_exception import SliseException


class SliseWindow:

    def __init__(self):
        self.path=None
        ui_file=os.path.dirname(os.path.realpath(__file__)) +\
            "/gui/slise.glade"

        if os.path.exists(ui_file):
            print 'found glade...'

        builder=gtk.Builder()
        builder.add_from_file(ui_file)

        #main window
        window=builder.get_object('window1')
        window.connect('delete-event',self.onExit)

        #file chooser dialog box
        select_file=builder.get_object('file_chooser')
        select_file.set_name('file')
        #on selection of file using FileChooseDialog box it generates "file-set" signal
        select_file.connect('file-set',self.onSelectFile)
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

        #text entry
        self.entry=builder.get_object('entry1')

        #search widget
        search=builder.get_object('search')
        search.connect('clicked',self.search)

        #image previews
        self.icon_view=builder.get_object('result_view')
        self.liststore=builder.get_object('icon_list')
        self.icon_view.set_model(self.liststore)
        self.icon_view.set_pixbuf_column(0)
        self.icon_view.set_text_column(1)

        self.icon_view.set_name('view')
        self.area.set_name('da')
        #add CSS
        style=gtk.CssProvider()
        style.load_from_path('./gui/style.css')
        gtk.StyleContext.add_provider_for_screen(gdk.Screen.get_default(),\
                                                 style,\
                                                 gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        window.show_all()

    def search(self,event):
        try:
            find_thread=ThreadPool(4)
            res=find_thread.apply_async(compare_histo,[self.hist_calc])
            res.get(timeout=1)
            print __MATCHED_FILE__

            fill_preview=ThreadPool(4)
            res2=fill_preview.apply_async(fill_icon_view,[self.liststore])
            res2.get(timeout=1)

            self.icon_view.queue_draw()
        except Exception as e:
            print e

    def onExpose(self,area,context):
        global __IMAGE_PATH__
        global __HISTOGRAM__

        if __IMAGE_PATH__ is not None:
            pix=GdkPixbuf.Pixbuf()
            img=pix.new_from_file_at_scale(__IMAGE_PATH__,300,300,1)
            gdk.cairo_set_source_pixbuf(context,img,0,0)
            context.fill()
            context.paint()

        if __HISTOGRAM__ is None and __IMAGE_PATH__ is not None :
            adjust_image=Adjust()
            adjust_image.image=cv2.imread(__IMAGE_PATH__)
            adjust_image.resize()
            adjust_image.tohsv(adjust_image.resized)
            self.hist_calc=Histogram(adjust_image.hsv)
            self.hist_calc.get_histogram()
            __HISTOGRAM__=self.hist_calc.draw_histogram()
            #print __HISTOGRAM__
            self.histogram.queue_draw()

    def drawHistogram(self,area,context):
        global __HISTOGRAM__
        if __HISTOGRAM__ is not None:
            pix=GdkPixbuf.Pixbuf()
            img=pix.new_from_data(__HISTOGRAM__.tostring(),\
                                  GdkPixbuf.Colorspace.RGB,\
                                  False,8,\
                                  __HISTOGRAM__.shape[1],\
                                  __HISTOGRAM__.shape[0],\
                                  __HISTOGRAM__.shape[1]*3,\
                                  None,None)
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
            self.entry.set_text(__FOLDER_PATH__)

    def gather_files(self,path):
        global __FILES__
        try:
            t=ThreadPool(4)
            res=t.apply_async(enumerate_files, [path])
            res.get(timeout=1)
            print 'thread created',__FILES__
        except Exception as e:
            print 'Unable to start enumeration thread',e

    def onExit(self,event,data):
        print 'Bye...',event,data
        gtk.main_quit()

def enumerate_files(path):
        global __FILES__
        print 'function called'

        folder_to_scan=[path]
        image_paths=[]

        while len(folder_to_scan):
            path_to_scan=folder_to_scan.pop()

            for f in os.listdir(str(path_to_scan)):
                if os.path.isfile(os.path.join(str(path_to_scan),f)):
                    name,ext=os.path.splitext(os.path.join(str(path_to_scan),f))
                    if ext.lower() in ('.jpg','.png','.jpeg'):
                        image_paths.append(os.path.join(str(path_to_scan),f))
                else:
                    folder_to_scan.append(os.path.join(str(path_to_scan),f))

        __FILES__=image_paths


def compare_histo(histo1):
    global __CURR_FILE__
    global __FILES__
    global __MATCHED_FILE__

    new_img=Adjust()

    while len(__FILES__):
        print len(__FILES__),
        __CURR_FILE__=__FILES__.pop()
        print 'current file',__CURR_FILE__

        try:
            new_img.image=cv2.imread(__CURR_FILE__)
            new_img.resize()
            new_img.tohsv(new_img.resized)
        except SliseException as Se:
            print Se
            continue

        new_hist=Histogram(new_img.hsv)
        new_hist.get_histogram()

        if histo1==new_hist:
            print 'yes',__CURR_FILE__
            __MATCHED_FILE__.append(__CURR_FILE__)

def fill_icon_view(liststore):
    if len(liststore)!=0:
        print 'its not empty'
            
    pix=GdkPixbuf.Pixbuf()
    while len(__MATCHED_FILE__):
        temp_name=__MATCHED_FILE__.pop()
        liststore.append(\
                         [pix.new_from_file_at_scale(temp_name,200,200,1),\
                          str(temp_name)])


if __name__=="__main__":
    SliseWindow()
    gtk.main()
        
    
