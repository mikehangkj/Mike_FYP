import tkinter as tk
from robomaster import robot
from PIL import ImageTk, Image
import cv2
import os
from time import sleep
from datetime import datetime
import sys
from sys import platform
import numpy as np
import time
import matplotlib.pyplot as plt
from twilio.rest import Client
import pyaudio

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_camera = ep_robot.camera
    capture = ep_camera.start_video_stream(display=False)
    print("capture:",capture)


value=0
sms=0
# count1=0
T=0.05 #tolerance
count=0
x=0

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.add_dll_directory(r"C:\openpose-master\build\x64\Release")
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # # Flags
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    # args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../../models/"
    params["hand"] = False
    params["face"] = False
    # params["video"]=True
    # params["frame_rotate"]=90
    params["fullscreen"] = True
    params["number_people_max"] = 2
    params["disable_blending"] = False   # for black background
    params["keypoint_scale"] = 3
    # params["display"] = 0

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    # print(datum)

except Exception as e:
    print(e)
    sys.exit(-1)

def play_audio():
    print("playing audio")
    # ep_robot.play_audio(filename="output6.wav").wait_for_completed()
    ep_robot.play_audio(filename="gtts2.wav").wait_for_completed()

def turn_on_rm_mic():
    global x,start,stop
    audio_player = pyaudio.PyAudio()
    playing_stream = audio_player.open(format=pyaudio.paInt16,channels=1,rate=48000,output=True)
    ep_camera.start_audio_stream()
    # print("main 1")
    # playing_task = threading.Thread(target=audio_playing_task, args=(ep_robot,))
    start=time.time()
    while x<200: #1000 counts is 20 secounds
        try:
            frame = ep_camera.read_audio_frame()
            # print("task 2")
            # print(frame)
        except Exception as e:
            print("LiveView: playing_task, video_frame_queue is empty.")
            continue
        # print("task 3")
        playing_stream.write(frame)
        x+=1
        # print("writing frame")
    x=0
    playing_stream.stop_stream()
    playing_stream.close()
    # ep_camera.stop_audio_stream()
    stop=time.time()


def video_stream():
    # datum = op.Datum()
    global count,sms,value,datum
    # img = ep_camera.read_cv2_image(strategy="newest")
    # sleep(0.1)
    if value==1:
        img = ep_camera.read_cv2_image(strategy="newest")
        sleep(0.1)
        # datum=op.Datum()
        datum.cvInputData = img
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        opframe = datum.cvOutputData

        try:
            if datum.poseKeypoints.any() != None:

                # print(str(datum.poseKeypoints))
                keypoint_1_data = datum.poseKeypoints[0, 1, :]
                keypoint_8_data = datum.poseKeypoints[0, 8, :]

                print("keypoint 1 data", keypoint_1_data)
                print("keypoint 8 data", keypoint_8_data)

                # print(type(keypoint_1_data[1]))
                #convert from pixels to 0 to 1 scale
                # keypoint_1_data[1]=keypoint_1_data[1]/720
                # keypoint_8_data[1]=keypoint_8_data[1]/720

                # print('keypoint 1 data',keypoint_1_data[1])
                # print('keypoint 8 data',keypoint_8_data[1])

                # print("count:",count)
                # if count == 0:
                #     # kp_0_data = np.array([keypoint_0_data])
                #     kp_1_data = np.array([keypoint_1_data])
                #     kp_8_data = np.array([keypoint_8_data])
                #
                #     # print("kp 1 data",kp_1_data)
                #     # print("kp 8 data",kp_8_data)
                #
                # else:
                #     # kp_0_data = np.insert(kp_0_data, [kp_0_data.shape[0]],[keypoint_0_data],axis=0)
                #     kp_1_data = np.insert(kp_1_data, [kp_1_data.shape[0]], [keypoint_1_data], axis=0)
                #     kp_8_data = np.insert(kp_8_data, [kp_8_data.shape[0]], [keypoint_8_data], axis=0)

                # print("kp_1-data shape:", kp_1_data.shape)
                # print("kp_8-data shape:", kp_8_data.shape)

                # print("keypoint 1 data:", keypoint_1_data)
                # print("keypoint 8 data:", keypoint_8_data)

                # print("kp_1_data", kp_1_data)
                # print("kp_8_data", kp_8_data)
                #
                # print("keypoint 1 data:",keypoint_1_data)
                # print("keypoint 8 data:",keypoint_8_data)

                if keypoint_1_data[1] > keypoint_8_data[1]:
                    if keypoint_1_data[1] - keypoint_8_data[1] < T:
                        # print(keypoint_1_data[1] - keypoint_8_data[1])
                        # print("1")
                        print("person is lying down")
                        sms += 1

                        while sms == 20:
                            # message = Client.messages.create(to="+6596930075", from_="+1 818 485 4907",
                            #                                  body="the person is lying down!")
                            print("playing audio")
                            play_audio()
                            turn_on_rm_mic()
                            sms = 0

                    elif keypoint_1_data[1] - keypoint_8_data[1] >= T:
                        # print(keypoint_1_data[1] - keypoint_8_data[1])
                        # print(datum.poseKeypoints)

                        print("person is not lying down")
                else:
                    pass

                if keypoint_8_data[1] > keypoint_1_data[1]:
                    if keypoint_8_data[1] - keypoint_1_data[1] < T:
                        # print(keypoint_8_data[1] - keypoint_1_data[1])
                        print("person is lying down")
                        sms += 1

                        while sms == 20:
                            # message = Client.messages.create(to="+6596930075", from_="+1 818 485 4907",
                            #                                  body="the person is lying down!")
                            print("playing audio")
                            play_audio()
                            # turn_on_rm_mic()
                            sms = 0

                    elif keypoint_8_data[1] - keypoint_1_data[1] >= T:
                        # print(datum.poseKeypoints)
                        # print("2")
                        print("person is not lying down")
                else:
                    pass

            cv2image = cv2.cvtColor(opframe, cv2.COLOR_BGR2RGB)
            opframe = Image.fromarray(cv2image, "RGB")
            imgtk = ImageTk.PhotoImage(image=opframe)
            main_label.imgtk = imgtk
            main_label.configure(image=imgtk)
            main_label.after(1, video_stream)

        except:
            pass
            print("no object detected")
            cv2image = cv2.cvtColor(opframe, cv2.COLOR_BGR2RGB)
            opframe = Image.fromarray(cv2image, "RGB")
            imgtk = ImageTk.PhotoImage(image=opframe)
            main_label.imgtk = imgtk
            main_label.configure(image=imgtk)
            main_label.after(1, video_stream)

    else:
        img = ep_camera.read_cv2_image(strategy="newest")
        # img = ep_camera.read_cv2_image()
        cv2image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img=Image.fromarray(cv2image,"RGB")
        imgtk=ImageTk.PhotoImage(image=img)
        main_label.imgtk=imgtk
        main_label.configure(image=imgtk)
        # video.after(20,video_stream)
        main_label.after(1,video_stream)

def button_pressed():
    global value
    value += 1
    print("toggle op")
    if value == 2:
        print("reset value")
        value=0
    else:
        pass

window=tk.Tk()
window.geometry("1300x750")

app=tk.Frame(window,bg="white")
app.place(relwidth=1,relheight=1)

main_label=tk.Label(app)
main_label.place(relheight=0.5,relwidth=0.5)

button=tk.Button(app,text="snapshot")
button.place(rely=0.5,relheight=0.1,relwidth=0.5)
# button.bind("<Button-1>",button_press)

button1=tk.Button(app,text="on vs",command=video_stream)
button1.place(rely=0.6,relheight=0.1,relwidth=0.5)

button2=tk.Button(app,text="toggle op",command=button_pressed)
button2.place(rely=0.7,relheight=0.1,relwidth=0.5)

# video_stream()
window.mainloop()
