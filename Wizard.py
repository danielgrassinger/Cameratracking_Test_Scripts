import tkinter as tk
from tkinter import *
from tkinter import messagebox
import cv2
import configparser
from PIL import Image, ImageTk
import threading
from threading import Thread
from time import sleep
import numpy as np


class IOSettings(Frame):
    def __init__(self, parent, controller,config):
        Frame.__init__(self, parent, width=640, height=480)
        self.controller = controller
        self.config = config

        self.pill2kill = threading.Event()

        Label(self, text='VideoInput ').grid(row=0, column=0)
        self.videoInput = Entry(self)
        self.videoInput.insert(0,self.config['Input']['videoinput'])

        self.videoInput.grid(row=0, column=1)
        testButton = Button(self,text='Test',command=self.start_preview)
        testButton.grid(row=0, column=2)

        self.liveVideo = Label(self, bg='black')
        self.liveVideo.grid(row=1, column=0, columnspan=3, sticky='WE')

        Label(self, text='Screen Output ').grid(row=2, column=0)
        self.screenOutputVar = IntVar()
        self.screenOutput = Checkbutton(self,variable=self.screenOutputVar)
        self.screenOutput.grid(row=2, column=1,sticky='W')
        self.screenOutput.var = self.screenOutputVar

        if self.config.getboolean('Output','screenoutput'):
            self.screenOutput.select()
        else:
            self.screenOutput.deselect()

    def start_preview(self):
        try:
            self.pill2kill.set()

            self.pill2kill = threading.Event()
            videoinput = self.videoInput.get()
            self.config['Input']['videoinput']=videoinput
            self.cap = cv2.VideoCapture((int(videoinput) if videoinput.isdigit() else videoinput ))
            self.cap.set(cv2.CAP_PROP_FPS, 30)

            self.video_thread = Thread(target=self.video_loop, args=(self.pill2kill, self.liveVideo, self.cap))
            self.video_thread.start()
            #sleep(3)
            #self.pill2kill.set()
            #self.video_thread.join()
        except Exception:
            pass

    def video_loop(self,stop_event, image_frame, cap):
        try:
            while not stop_event.is_set():
                ret, frame = cap.read()
                # frame = cv2.imread('assets/Test3.jpg')
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(frame_rgb)
                    imgtk = ImageTk.PhotoImage(image=im)

                    # Put it in the display window
                    image_frame.configure(image=imgtk)
                    image_frame.image = imgtk
                sleep(0.03)

        except RuntimeError:
            pass
    def releaseCamera(self):
        try:
            self.pill2kill.set()
            self.cap.release()
        except AttributeError:
            pass

    def save_settings(self):
        self.config['Input']['videoinput']=self.videoInput.get()
        self.config['Output']['screenoutput']=str(True if self.screenOutputVar.get() else False)

class ServerSettings(Frame):
    def __init__(self, parent, controller,config):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config=config


        Label(self, text='Write Database').grid(row=0,column=0)
        self.writeDatabaseVar = IntVar()
        writeDatabase=Checkbutton(self,variable=self.writeDatabaseVar)
        writeDatabase.grid(row=0,column=1,sticky='W')

        if self.config.getboolean('BackendServer','writedatabase')==True:
            writeDatabase.select()
            pass
        else:
            writeDatabase.deselect()
            pass

        Label(self, text='Server IP').grid(row=1,column=0)
        self.serverIP = Entry(self)
        self.serverIP.insert(0,self.config['BackendServer']['serverip'])
        self.serverIP.grid(row=1,column=1)

        Label(self, text='Server Port').grid(row=2, column=0)
        self.serverPort = Entry(self)
        self.serverPort.insert(0, self.config['BackendServer']['serverport'])
        self.serverPort.grid(row=2, column=1)

        Label(self, text='Server Script URL').grid(row=3, column=0)
        self.serverScriptURL = Entry(self)
        self.serverScriptURL.insert(0,self.config['BackendServer']['serverscripturl'])
        self.serverScriptURL.grid(row=3, column=1)

    def save_settings(self):
        self.config['BackendServer']['WriteDatabase'] = str(True if self.writeDatabaseVar.get() else False)
        self.config['BackendServer']['serverip'] = self.serverIP.get()
        self.config['BackendServer']['serverport'] = self.serverPort.get()
        self.config['BackendServer']['serverscripturl'] = self.serverScriptURL.get()



class DrawerSettings(Frame):

    def __init__(self, parent, controller,config):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config = config

        up = Button(self, text='^',command=self.up)
        up.grid(row=1,column=0)
        down = Button(self, text='v',command=self.down)
        down.grid(row=2,column=0)

        Label(self, text='Drawers').grid(row=0,column=1)

        drawers = self.config['Drawers']['drawers']
        drawers.strip()
        drawers = drawers.replace('[','')
        drawers = drawers.replace(']','')
        drawers.replace(']','')
        drawers = drawers.split(',')
        for i in range(len(drawers)):
            drawers[i] = drawers[i].strip()

        self.listbox = Listbox(self)


        for x in drawers:
            self.listbox.insert(END,x)

        self.listbox.grid(row=1,column=1,rowspan=4)

        create = Button(self,text='New',command=self.create)
        create.grid(row=1,column=2)
        edit = Button(self, text='Change',command=self.edit)
        edit.grid(row=2,column=2)
        delete = Button(self, text='Delete',command=self.delete)
        delete.grid(row=3, column=2)

    def create(self):

        createWindow = ToolSettings(self.controller,self.config)
        createWindow.grab_set()
        createWindow.wait_window(createWindow)
        name = createWindow.getDrawerName()
        if(name != None):
            self.listbox.insert(END, name)


    def edit(self):
        if (len(self.listbox.curselection()) > 0):
            selected = self.listbox.curselection()[0]
            createWindow = ToolSettings(self.controller, self.config, drawerName=self.listbox.get(selected))
            createWindow.grab_set()
            createWindow.wait_window(createWindow)
            name = createWindow.getDrawerName()
            if (name != None):
                self.listbox.delete(selected)
                self.listbox.insert(selected, name)

    def delete(self):
        if(len(self.listbox.curselection()) >0):
            self.config.remove_section(self.listbox.get(self.listbox.curselection()[0]))
            self.listbox.delete(self.listbox.curselection()[0])


    def up(self):
        index = self.listbox.curselection()[0]
        if index > 0:
            save = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index-1,save)
            self.listbox.select_set(index - 1)

    def down(self):
        index = self.listbox.curselection()[0]
        if index < self.listbox.size()-1:
            save = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index +1, save)
            self.listbox.select_set(index +1)

    def save_settings(self):
        list_string = '['
        for i in self.listbox.get(0,END):
            list_string = list_string + i + ', '
        list_string = list_string[:-2] + ']'
        self.config['Drawers']['drawers'] = list_string


class ToolSettings(Toplevel):
    def __init__(self, parent,config,drawerName='Unnamed'):
        Toplevel.__init__(self, parent)

        self.config = config
        self.controller = parent
        self.drawerName = drawerName

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        Label(self,text='Drawer Name').grid(row=0,column=0)
        self.drawerNameEntry = Entry(self)
        self.drawerNameEntry.insert(0,drawerName)
        self.drawerNameEntry.grid(row=0,column=1)

        Label(self,text='Drawer Detection Field').grid(row=1,column=0)
        Button(self, text='Configure ...', command=self.configureDetectionField).grid(row=1,column=1)

        Label(self, text='Tools').grid(row=3, column=0)
        l = ['Suchblade1', 'Schublade 2', 'Schublade3']

        self.listbox = Listbox(self)

        if(self.drawerName in config.sections()):
            tools = self.config[self.drawerName]['tools']
            tools.strip()
            tools = tools.replace('[', '')
            tools = tools.replace(']', '')
            tools.replace(']', '')
            tools = tools.split(',')
            for i in range(len(tools)):
                tools[i] = tools[i].strip()

            for x in tools:
                self.listbox.insert(END,x)

        self.listbox.grid(row=2,column=1,rowspan=4)

        create = Button(self,text='New',command=self.create)
        create.grid(row=2,column=2)
        change = Button(self, text='Change',command=self.edit)
        change.grid(row=3,column=2)
        delete = Button(self, text='Delete',command=self.delete)
        delete.grid(row=4, column=2)

        Button(self, text='Save', command=self.save).grid(row=6,column=1)
        Button(self, text='Cancel', command=self.cancel).grid(row=6,column=2)

    def save(self):
        self.drawerName =self.drawerNameEntry.get()
        if (self.drawerName not in self.config.sections()):
            self.config[self.drawerName] = {}
        list_string = '['
        for i in self.listbox.get(0, END):
            list_string = list_string + i + ', '
        list_string = list_string[:-2] + ']'
        self.config[self.drawerName]['tools'] = list_string
        self.destroy()

    def cancel(self):
        self.drawerName = None
        self.destroy()

    def configureDetectionField(self):
        self.drawerName = self.drawerNameEntry.get()
        window = DetectionFieldSettings(self, self.config, self.drawerName)
        window.grab_set()
        window.wait_window(window)
    def getDrawerName(self):
        return self.drawerName

    def create(self):

        createWindow = ToolPositionSettings(self,self.config)
        createWindow.grab_set()
        createWindow.wait_window(createWindow)
        toolId = createWindow.getToolId()
        if(toolId != None):
            self.listbox.insert(END,toolId)


    def edit(self):
        if (len(self.listbox.curselection()) > 0):
            selected = self.listbox.curselection()[0]
            createWindow = ToolPositionSettings(self, self.config,toolId=self.listbox.get(selected))
            createWindow.grab_set()
            createWindow.wait_window(createWindow)
            toolId = createWindow.getToolId()
            if (toolId != None):
                self.listbox.delete(selected)
                self.listbox.insert(selected, toolId)

    def delete(self):
        if(len(self.listbox.curselection()) >0):
            self.listbox.delete(self.listbox.curselection()[0])

class DetectionFieldSettings(Toplevel):

    def __init__(self,parent,config, drawerName):
        Toplevel.__init__(self,parent)
        self.config = config
        self.drawerName = drawerName

        self.leftupperx = 0
        self.leftuppery = 0
        self.rightdownx = 0
        self.rightdowny = 0
        self.x = 0
        self.y = 0

        if str(self.drawerName) in self.config.sections():
            self.leftupperx = int(self.config[self.drawerName]['leftupperx'])
            self.leftuppery = int(self.config[self.drawerName]['leftuppery'])
            self.rightdownx = int(self.config[self.drawerName]['rightdownx'])
            self.rightdowny = int(self.config[self.drawerName]['rightdowny'])
            self.x = int(self.config[self.drawerName]['rightdownx'])
            self.y = int(self.config[self.drawerName]['rightdowny'])
        else:
            self.config[self.drawerName] = {}



        self.protocol("WM_DELETE_WINDOW", self.cancel)

        Label(self,text='Hue min').grid(row=0,column=0)
        self.hue_min = Scale(self, from_=0, to=179, orient=HORIZONTAL)
        self.hue_min.set(int(self.config[self.drawerName]['hue_min']))
        self.hue_min.grid(row=0, column=1)

        Label(self, text='Hue max').grid(row=1, column=0)
        self.hue_max = Scale(self, from_=0, to = 179, orient=HORIZONTAL)
        self.hue_max.set(self.config[self.drawerName].getint('hue_max'))
        self.hue_max.grid(row=1, column=1)

        Label(self, text='Saturation').grid(row=2, column=0)
        self.saturation = Scale(self, from_=0, to = 255, orient=HORIZONTAL)
        self.saturation.set(self.config[self.drawerName].getint('saturation'))
        self.saturation.grid(row=2, column=1)

        Label(self, text='Value').grid(row=3, column=0)
        self.value = Scale(self, from_=0, to = 255, orient=HORIZONTAL)
        self.value.set(self.config[self.drawerName].getint('value'))
        self.value.grid(row=3, column=1)

        self.imageBox = Label(self, bg='black')
        self.imageBox.bind("<ButtonPress-1>", self.press)
        self.imageBox.bind("<B1-Motion>", self.hold)
        self.imageBox.bind("<ButtonRelease-1>", self.release)
        self.imageBox.grid(row=4,column=0, columnspan=2)

        Button(self,text='Save',command=self.save).grid(row=5, column=0)
        Button(self,text='Cancel',command=self.cancel).grid(row=5,column=1)
        self.pill2kill = threading.Event()
        self.start_preview()

    def press(self,event):
        self.leftupperx = event.x
        self.leftuppery = event.y
        self.x = event.x
        self.y = event.y
        #print('Leftupper ' + str(event.x) + ' '+ str(event.y))
    def hold(self,event):
        self.x = event.x
        self.y = event.y
    def release(self,event):
        self.rightdownx = event.x
        self.rightdowny = event.y
        #print('Rightdown ' + str(event.x) + ' ' + str(event.y))

    def start_preview(self):
        try:
            self.pill2kill.set()

            self.pill2kill = threading.Event()
            videoinput = self.config['Input']['videoinput']
            self.cap = cv2.VideoCapture((int(videoinput) if videoinput.isdigit() else videoinput ))

            self.video_thread = Thread(target=self.video_loop, args=(self.pill2kill, self.imageBox, self.cap))
            self.video_thread.start()

        except Exception:
            pass

    def video_loop(self,stop_event, image_frame, cap):
        try:
            while not stop_event.is_set():
                ret, frame = cap.read()
                # frame = cv2.imread('assets/Test3.jpg')
                if ret:
                    frame,mask = self.colorFilterHSV(frame,(self.hue_min.get(),self.saturation.get(),self.value.get()),(self.hue_max.get(),255,255))
                    #frame,mask = self.colorFilterHSV(image=frame)
                    cv2.rectangle(frame, (self.leftupperx, self.leftuppery), (self.x, self.y), (0, 0, 255), 2)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(frame_rgb)
                    imgtk = ImageTk.PhotoImage(image=im)

                    # Put it in the display window
                    image_frame.configure(image=imgtk)
                    image_frame.image = imgtk
                sleep(0.03)

        except RuntimeError:
            pass

    def colorFilterHSV(self,image, hsv_min=(0, 0, 0), hsv_max=(180, 255, 255)):

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_color = np.array(hsv_min)
        upper_color = np.array(hsv_max)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv_image, lower_color, upper_color)

        # Bitwise-AND mask and original image
        result = cv2.bitwise_and(image, image, mask=mask)

        return result, mask

    def releaseCamera(self):
        try:
            self.pill2kill.set()
            self.cap.release()
        except AttributeError:
            pass

    def save(self):
        if(self.drawerName not in self.config.sections()):
            self.config[self.drawerName] ={}
        self.config[self.drawerName]['hue_min'] = str(self.hue_min.get())
        self.config[self.drawerName]['hue_max'] = str(self.hue_max.get())
        self.config[self.drawerName]['saturation'] = str(self.saturation.get())
        self.config[self.drawerName]['value'] = str(self.value.get())

        self.config[self.drawerName]['leftupperx'] = str(self.leftupperx)
        self.config[self.drawerName]['leftuppery'] = str(self.leftuppery)
        self.config[self.drawerName]['rightdownx'] = str(self.rightdownx)
        self.config[self.drawerName]['rightdowny'] = str(self.rightdowny)

        self.releaseCamera()
        self.destroy()

    def cancel(self):
        self.releaseCamera()
        self.destroy()

class ToolPositionSettings(Toplevel):

    def __init__(self,parent, config,toolId='0'):
        Toplevel.__init__(self,parent)

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.config = config
        self.toolId = toolId

        self.leftupperx = 0
        self.leftuppery = 0
        self.rightdownx = 0
        self.rightdowny = 0
        self.x = 0
        self.y = 0

        if (self.toolId in self.config.sections()):
            self.leftupperx = int(self.config[self.toolId]['leftupperx'])
            self.leftuppery = int(self.config[self.toolId]['leftuppery'])
            self.rightdownx = int(self.config[self.toolId]['rightdownx'])
            self.rightdowny = int(self.config[self.toolId]['rightdowny'])
            self.x = int(self.config[self.toolId]['rightdownx'])
            self.y = int(self.config[self.toolId]['rightdowny'])



        Label(self,text='Tool ID').grid(row=0,column=0)
        self.id = Entry(self)
        self.id.insert(0,self.toolId)
        self.id.grid(row=0,column=1)

        Label(self, text='Please mark the tool with the mouse in the video screen').grid(row=1,column=0, columnspan=2)
        self.imageBox = Label(self)
        self.imageBox.bind("<ButtonPress-1>", self.press)
        self.imageBox.bind("<B1-Motion>", self.hold)
        self.imageBox.bind("<ButtonRelease-1>", self.release)
        self.imageBox.grid(row=2,column=0,columnspan=2)

        Button(self, text='Save', command=self.save).grid(row=3, column=0)
        Button(self, text='Cancel', command=self.cancel).grid(row=3, column=1)
        self.pill2kill = threading.Event()
        self.start_preview()

    def press(self,event):
        self.leftupperx = event.x
        self.leftuppery = event.y
        self.x = event.x
        self.y = event.y
        #print('Leftupper ' + str(event.x) + ' '+ str(event.y))
    def hold(self,event):
        self.x = event.x
        self.y = event.y
    def release(self,event):
        self.rightdownx = event.x
        self.rightdowny = event.y
        #print('Rightdown ' + str(event.x) + ' ' + str(event.y))

    def start_preview(self):
        try:
            self.pill2kill.set()

            self.pill2kill = threading.Event()
            videoinput = self.config['Input']['videoinput']
            self.cap = cv2.VideoCapture((int(videoinput) if videoinput.isdigit() else videoinput ))

            self.video_thread = Thread(target=self.video_loop, args=(self.pill2kill, self.imageBox, self.cap))
            self.video_thread.start()

        except Exception:
            pass

    def video_loop(self,stop_event, image_frame, cap):
        try:
            while not stop_event.is_set():
                ret, frame = cap.read()

                if ret:
                    cv2.rectangle(frame, (self.leftupperx,self.leftuppery), (self.x,self.y), (0, 0, 255), 2)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(frame_rgb)
                    imgtk = ImageTk.PhotoImage(image=im)

                    # Put it in the display window
                    image_frame.configure(image=imgtk)
                    image_frame.image = imgtk
                sleep(0.03)

        except RuntimeError:
            pass
    def releaseCamera(self):
        try:
            self.pill2kill.set()
            self.cap.release()
        except AttributeError:
            pass

    def getToolId(self):
        return self.toolId

    def save(self):
        self.toolId = self.id.get()

        if(self.toolId not in self.config.sections()):
            self.config[self.toolId] = {}
        self.config[self.toolId]['leftupperx'] = str(self.leftupperx)
        self.config[self.toolId]['leftuppery'] = str(self.leftuppery)
        self.config[self.toolId]['rightdownx'] = str(self.rightdownx)
        self.config[self.toolId]['rightdowny'] = str(self.rightdowny)

        self.releaseCamera()
        self.destroy()

    def cancel(self):
        self.toolId = None
        self.releaseCamera()
        self.destroy()

class Wizard(Tk):

    def __init__(self, config):
        Tk.__init__(self)
        self.title('Konfigurationswizard')
        self.config = config
        self.protocol("WM_DELETE_WINDOW", self.cancel)




        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        navigation = Frame(self).pack(side='bottom')
        self.cancelButton = Button(navigation, text='Cancel', command=self.cancel)
        self.cancelButton.pack(side='right')

        self.finishButton = Button(navigation, text="Finish", command=self.finish)
        self.finishButton.pack(side='right')
        self.forwardButton = Button(navigation, text="Next >", command=self.next)
        self.forwardButton.pack(side='right')
        self.backButton = Button(navigation, text="< Back",command=self.back)
        self.backButton.pack(side='right')
        self.backButton.config(state='disable')

        self.statecounter=0
        self.frames = {}
        self.states = (IOSettings, ServerSettings, DrawerSettings)
        for F in self.states:
            page_name = F.__name__
            frame = F(parent=container, controller=self,config=config)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("IOSettings")

    def back(self):
        self.statecounter = self.statecounter -1
        self.forwardButton.config(state='normal')
        if(self.statecounter==0):
            # disable back button
            self.backButton.config(state='disable')
        self.show_frame(self.states[self.statecounter].__name__)

    def next(self):
        self.statecounter = self.statecounter +1
        self.backButton.config(state='normal')
        if(self.statecounter==len(self.states)-1):
            self.forwardButton.config(state='disable')
        self.frames['IOSettings'].releaseCamera()
        self.show_frame(self.states[self.statecounter].__name__)

    def finish(self):
        if messagebox.askyesno('Save', 'Do you want to save the settings?'):

            for state in self.frames:
                self.frames[state].save_settings()
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            self.frames['IOSettings'].releaseCamera()
            self.destroy()
        else:
            pass

    def cancel(self):
        if messagebox.askyesno('Quit', 'Do you want to quit without saving?'):
            self.frames['IOSettings'].releaseCamera()
            self.destroy()
        else:
            pass


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    #for i in config.sections():
        #print(i)
    wizard = Wizard(config)
    wizard.mainloop()


if __name__ == "__main__":
    main()