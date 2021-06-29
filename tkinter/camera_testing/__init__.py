import tkinter
import cv2
import PIL.Image,PIL.ImageTk
import time

class App:
    def __init__(self,window,window_title,video_source=0):
        self.window=window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid=MyVideoCapture(video_source)

        self.canvas=tkinter.Canvas(window,width=self.vid.width,height=self.vid.height)
        self.canvas.pack()

        self.btn_snapshot=tkinter.Button(window, text="Snapshot",width=50,command=self.snap)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.delay=15
        self.update()

        self.window.mainloop()


    def update(self):
        ret,frame=self.vid.get_frame()

        if ret:
            self.photo=PIL.ImageTK.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image=self.photo,anchor=tkinter.NW)

        self.window.after(self.delay,self.update)

    def snapshot(self):
        ret,frame=self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-"+ time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

class MyVideoCapture:
    def __init__(self,video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source",video_source)

        self.width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.mainloop()

    def get_frame(self):
        if self.vid.isOpened():
            ret,frame=self.vid.read()
            if ret:
                return(ret,cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            else:
                return(ret,None)
        else:
            return(ret,None)



App(tkinter.Tk(),"Tkinter and OpenCV")
