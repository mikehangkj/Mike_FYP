# from __future__ import print_function
# from PIL import Image,ImangeTk
# import tkinter as tk
# import threading
# import datetime
# import imutils
# import cv2
# import os
#
# class PhotoBoothApp:
#     def __init__(self, vs, outputPath):
#         self.vs=vs
#         self.outputPath=outputPath
#         self.frame=None
#         self.thread=None
#         self.stopEvent=None
#
#         self.root=tk.Tk()
#         self.panel=None
#
# btn=tk.Button(self.root,text="Snapshot!",command=self.takeSnapshot)
# btn.pack(side="bottom",fill="both",expend="yes",padx=10,pady=10)
#
# self.stopEvent = threading.Event()
# self.thread= threading.Thread(target= self.videoLoop,agrs=())
# self.thread.start()
#
# self.root.wm_title("PyImageSearch PhotoBooth")
# self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
#
#
# def videoLoop(self):
#     try:
#         while not self.stopEvent.is_set():
#             self.frame=self.vs.read()
#             self.frame=imutils.resize(self.frame,width=300)
#
#             image=cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
#
