from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import os.path
from functools import partial
from queue import Queue
from threading import Thread
import threading


def save_image(queue):
    image_path = 'saves/image_'
    file_extension = '.png'

    i = 0
    while os.path.exists(image_path + str(i) + file_extension):
        i = i + 1

    while queue.qsize()>1:
        queue.get()
    cv2.imwrite(image_path + str(i) + file_extension, queue.get())
    print(image_path + str(i) + file_extension)
    print('Image saved')


def save_video(save_video_button,queue):
    if(save_video_button.cget('text')=='Start Video Recording'):
        save_video_button.config(text='Stop Video Recording')
        queue.queue.clear()


    elif(save_video_button.cget('text')=='Stop Video Recording'):
        save_video_button.config(text='Start Video Recording')

        video_path = 'saves/video_'
        file_extension = '.avi'

        i = 0
        while os.path.exists(video_path + str(i) + file_extension):
            i = i + 1

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        out = cv2.VideoWriter(video_path + str(i) + file_extension, fourcc, 20.0, (640, 480))

        while queue.qsize() > 0:
            out.write(queue.get())
        out.release()
        print('Video Saved')


def camera_settings(root,cap):
    settings_string = ['CV_CAP_PROP_POS_MSEC','CV_CAP_PROP_POS_FRAMES', 'CV_CAP_PROP_POS_AVI_RATIO', 'CV_CAP_PROP_FRAME_WIDTH', 'CV_CAP_PROP_FRAME_HEIGHT',
                           'CV_CAP_PROP_FPS', 'CV_CAP_PROP_FOURCC', 'CV_CAP_PROP_FRAME_COUNT', 'CV_CAP_PROP_FORMAT', 'CV_CAP_PROP_MODE', 'CV_CAP_PROP_BRIGHTNESS',
                           'CV_CAP_PROP_CONTRAST', 'CV_CAP_PROP_SATURATION', 'CV_CAP_PROP_HUE', 'CV_CAP_PROP_GAIN', 'CV_CAP_PROP_EXPOSURE',
                           'CV_CAP_PROP_CONVERT_RGB', 'CV_CAP_PROP_WHITE_BALANCE', 'CV_CAP_PROP_RECTIFICATION']
    window = Toplevel(root)
    window.title('Camera Settings')
    text = ''
    for i in range(20):
        try:
            text= text + str(i)+ '. ' +settings_string[i] + '\t'+str(cap.get(i))+'\n'
        except Exception:
            continue
    Label(window, text=text, justify=LEFT).pack()




def video_loop(stop_event, image_frame, cap, queue):
    try:
        while not stop_event.is_set():
            ret, frame = cap.read()
            # frame = cv2.imread('assets/Test3.jpg')
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=im)

            # Put it in the display window
            image_frame.configure(image=imgtk)
            image_frame.image = imgtk
            queue.put(frame)
    except RuntimeError:
        pass


def main():
    queue = Queue()
    #image = cv2.imread('assets/Test3.jpg')
    #image = cv2.resize(image, (480, 320))
    # Rearrang the color channel
    #b, g, r = cv2.split(image)
    #img = cv2.merge((r, g, b))

    # A root window for displaying objects
    root = Tk()
    root.title('Camera_Test')
    # root.geometry('900x700')

    cap = cv2.VideoCapture(1)
    cap.set(10,0.3)
    cap.set(11,0.3)
    save_image_button = Button(root, text='Bild speichern', command=partial(save_image, queue))
    save_video_button = Button(root, text='Start Video Recording')
    save_video_button.config(command = partial(save_video, save_video_button,queue))
    camera_settings_button = Button(root, text='Camera Einstellungen', command=partial(camera_settings,root,cap))

    # Convert the Image object into a TkPhoto object
    #im = Image.fromarray(img)
    #imgtk = ImageTk.PhotoImage(image=im)

    # Put it in the display window
    image_frame = Label(root)

    image_frame.pack()
    save_image_button.pack(side=LEFT)
    save_video_button.pack(side=LEFT)
    camera_settings_button.pack(side=RIGHT)



    pill2kill = threading.Event()

    video_thread = Thread(target=video_loop, args=(pill2kill, image_frame, cap, queue))
    video_thread.start()

    root.mainloop()  # Start the GUI

    pill2kill.set()
    video_thread.join()

    while (video_thread.isAlive):
        pass
    print('End')
    cap.release()


if __name__ == "__main__":
    main()
