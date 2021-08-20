import tkinter as tk
from robomaster import robot
from PIL import ImageTk, Image
import cv2
import os
from time import sleep
from datetime import datetime
import time
import pyaudio
from tkinter.messagebox import showinfo


#robomaster chassis controls
x_val=0.2 #forward distance
y_val=0.2 #sideways distance
z_val=10 #distance of turn
xy_s=5 #speed of forward and sideways m/s
z_s=30 #speed of turn degrees/s

#movement button controls size
w=0.33
h=0.24
# w=0.25
# h=0.20

x=0 #mic time count
count=0

#initialise robot
if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_camera=ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_arm = ep_robot.robotic_arm
    ep_gripper = ep_robot.gripper

    # ep_camera.start_audio_stream()
    capture = ep_camera.start_video_stream(display=False)

#movement functions
def move_foward():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=x_val,y=0,z=0,xy_speed=xy_s).wait_for_completed()
    # print("moving forward")

def move_backward():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=-x_val,y=0,z=0,xy_speed=xy_s).wait_for_completed()
    # print("moving backwards")

def move_right():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=0,y=y_val,z=0,xy_speed=xy_s).wait_for_completed()
    # print("moving right")

def move_left():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=0,y=-y_val,z=0,xy_speed=xy_s).wait_for_completed()
    # print("moving left")

def move_foward_left():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=x_val,y=-y_val,z=0,xy_speed=xy_s).wait_for_completed()
    # print("moving forward and left")

def move_foward_right():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=x_val,y=y_val,z=0,xy_speed=xy_s).wait_for_completed()
    # print("moving forward and right")

def move_backward_left():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=-x_val,y=-y_val,z=0,xy_speed=xy_s).wait_for_completed()
    # print("moving backwards and left")

def move_backward_right():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=-x_val,y=y_val,z=0,xy_speed=xy_s).wait_for_completed()
    # print("moving backwards and right")

def left_turn():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=0,y=0,z=z_val,z_speed=z_s).wait_for_completed()
    # print("left turn")

def right_turn():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=0,y=0,z=-z_val,z_speed=z_s).wait_for_completed()
    # print("right turn")

#robotic arm movement function
def arm_move_up():
    ep_arm.move(y=20).wait_for_completed()

def arm_move_down():
    ep_arm.move(y=-20).wait_for_completed()

#gripper movement function
def gripper_move_fw():
    ep_arm.move(x=20).wait_for_completed()

def gripper_move_bw():
    ep_arm.move(x=-20).wait_for_completed()

def gripper_open():
    ep_gripper.open(power=50)
    sleep(1)

def gripper_close():
    ep_gripper.close(power=50)
    sleep(1)

#video stream function
def video_stream():
    img = ep_camera.read_cv2_image(strategy="newest")
    # img = ep_camera.read_cv2_image()
    cv2image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img=Image.fromarray(cv2image,"RGB")
    imgtk=ImageTk.PhotoImage(image=img)
    video.imgtk=imgtk
    video.configure(image=imgtk)
    # video.after(20,video_stream)
    video.after(1,video_stream)

#screenshot function
def screenshot(capture,path_output_dir):
    global count
    print("screenshot")
    print(count)
    # count=count
    # while capture.isOpened():
    while count<1000:
        img2=ep_camera.read_cv2_image()
        # cv2.imwrite(os.path.join(path_output_dir,'%d.png')%count,img2)
        time = int(datetime.now().strftime("%d%m%y%H%M%S"))
        cv2.imwrite(os.path.join(path_output_dir, '%d.png') %time, img2)
        count=count+1
        break

def button_press(event):
    screenshot(capture,r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\RM_screenshots")
    print("clicked")

#end program function
def stop_program():
    window.destroy()
    ep_camera.stop_video_stream()
    ep_robot.close()

def turn_on_rm_mic():
    global x,start,stop
    print("on mic")
    audio_player = pyaudio.PyAudio()
    playing_stream = audio_player.open(format=pyaudio.paInt16,channels=1,rate=48000,output=True)
    ep_camera.start_audio_stream()
    # print("main 1")
    # playing_task = threading.Thread(target=audio_playing_task, args=(ep_robot,))
    start=time.time()
    while x<1000: #1000 counts is 20 secounds
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
    print(str(stop-start) +"seconds")

def popup_showinfo():
    showinfo("ShowInfo", "warning! The person is lying down!")

def play_audio1():
    ep_robot.play_audio(filename="okay.wav").wait_for_completed()

def play_audio2():
    ep_robot.play_audio(filename="help.wav").wait_for_completed()

window = tk.Tk()
window.title("RoboMaster UI")

window.geometry("1920x1280")

#imported images
up_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\up_arrow.png")
down_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\down_arrow.png")
left_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\left_arrow.png")
right_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\right_arrow.png")
top_right_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\top_right_arrow.png")
top_left_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\top_left_arrow.png")
btm_right_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\btm_right_arrow.png")
btm_left_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\btm_left_arrow.png")
camera_pic=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\camera_pic.png")
left_turn_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\back_arrow.png")
right_turn_arrow=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\redo_arrow.png")
power_button=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\power_button.png")\

upward=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\fyp_pics\upward.png")
downward=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\fyp_pics\downward.png")
forward=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\fyp_pics\forward.png")
backward=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\fyp_pics\backward.png")
open_gripper_pic=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\open_gripper2.png")
close_gripper_pic=tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\close_gripper2.png")

display=tk.Frame(master=window,bg="black",width=100,height=30)
display.place(relwidth=0.6,relheight=0.6)

video=tk.Label(display,bg="black")
video.place(relwidth=1,relheight=0.9)

button=tk.Button(display,text="click to start stream",command=video_stream)
button.place(rely=0.9,relwidth=1,relheight=0.1)

#arm and gripper function
arm_gripper_frame=tk.Frame(master=window)
arm_gripper_frame.place(rely=0.65,relwidth=0.6,relheight=0.35)

arm_gripper_func_display=tk.Label(master=arm_gripper_frame,relief="ridge",text="arm and gripper controls")
arm_gripper_func_display.place(relwidth=1,relheight=0.1)

open_gripper=tk.Button(arm_gripper_frame,font=20,image=open_gripper_pic,command=gripper_open)
open_gripper.place(rely=0.1,relwidth=0.2,relheight=0.55)

open_gripper_label=tk.Label(arm_gripper_frame,text="open gripper",relief="sunken")
open_gripper_label.place(rely=0.65,relwidth=0.2,relheight=0.1)

close_gripper=tk.Button(arm_gripper_frame,font=20,image=close_gripper_pic,command=gripper_close)
close_gripper.place(relx=0.2,rely=0.1,relwidth=0.2,relheight=0.55)

close_gripper_label=tk.Label(arm_gripper_frame,text="close gripper",relief="sunken")
close_gripper_label.place(rely=0.65,relx=0.2,relwidth=0.2,relheight=0.1)

arm_up = tk.Button(master=arm_gripper_frame,font=20,image=upward,command=arm_move_up)
arm_up.place(relx=0.4,rely=0.1,relwidth=0.15,relheight=0.55)

arm_up_label=tk.Label(arm_gripper_frame,text="arm move upward",relief="sunken")
arm_up_label.place(rely=0.65,relx=0.4,relwidth=0.15,relheight=0.1)

arm_down = tk.Button(master=arm_gripper_frame,text="downward",font=20,image=downward,command=arm_move_down)
arm_down.place(relx=0.55,rely=0.1,relwidth=0.15,relheight=0.55)

arm_down_label=tk.Label(arm_gripper_frame,text="arm move downward",relief="sunken")
arm_down_label.place(rely=0.65,relx=0.55,relwidth=0.15,relheight=0.1)

gripper_forward=tk.Button(master=arm_gripper_frame,font=20,image=forward,command=gripper_move_fw)
gripper_forward.place(relx=0.7,rely=0.1,relwidth=0.15,relheight=0.55)

gripper_forward_label=tk.Label(arm_gripper_frame,text="forward gripper",relief="sunken")
gripper_forward_label.place(rely=0.65,relx=0.7,relwidth=0.15,relheight=0.1)

gripper_backward=tk.Button(master=arm_gripper_frame,font=20,image=backward,command=gripper_move_bw)
gripper_backward.place(relx=0.85,rely=0.1,relwidth=0.15,relheight=0.55)

gripper_backward_label=tk.Label(arm_gripper_frame,text="backward gripper",relief="sunken")
gripper_backward_label.place(rely=0.65,relx=0.85,relwidth=0.15,relheight=0.1)

audio_controls=tk.Frame(master=window)
audio_controls.place(relx=0.65,rely=0.1,relwidth=0.3,relheight=0.15)

audio1_btn=tk.Button(master=audio_controls,text="play okay",command=play_audio1)
audio1_btn.place(relwidth=w,relheight=1)

audio2_btn=tk.Button(master=audio_controls,text="play help",command=play_audio2)
audio2_btn.place(relx=0.335,relwidth=w,relheight=1)

# mic_on_btn=tk.Button(master=audio_controls,text="on rm mic",command=turn_on_rm_mic)
mic_on_btn=tk.Button(master=audio_controls,text="popup info",command=popup_showinfo)
mic_on_btn.place(relx=0.67,relwidth=w,relheight=1)

#right side buttons
button_controls=tk.Frame(master=window)
button_controls.place(relx=0.65,rely=0.3,relwidth=0.3,relheight=0.6)

left_turn_btn = tk.Button(master=button_controls,text="left turn",image=left_turn_arrow,command=left_turn)
left_turn_btn.place(relwidth=w,relheight=h)

camera_btn=tk.Button(master=button_controls,text="camera",image=camera_pic)
camera_btn.place(relx=0.335,relwidth=w,relheight=h)
camera_btn.bind("<Button-1>",button_press)

right_turn_btn = tk.Button(master=button_controls,text="right turn",image=right_turn_arrow,command=right_turn)
right_turn_btn.place(relx=0.67,relwidth=w,relheight=h)

forward_left_btn = tk.Button(master=button_controls,text="forward and left",image=top_left_arrow,command=move_foward_left)
forward_left_btn.place(rely=0.25,relwidth=w,relheight=h)

up_btn = tk.Button(master=button_controls,text="forward",image=up_arrow,command=move_foward)
up_btn.place(rely=0.25,relx=0.335,relwidth=w,relheight=h)

forward_right_btn = tk.Button(master=button_controls,text="forward and right",image=top_right_arrow,command=move_foward_right)
forward_right_btn.place(rely=0.25,relx=0.67,relwidth=w,relheight=h)

left_btn = tk.Button(master=button_controls,text="left",image=left_arrow,command=move_left)
left_btn.place(rely=0.5,relwidth=w,relheight=h)

off_btn=tk.Button(master=button_controls,text="off",image=power_button,command=stop_program)
off_btn.place(relx=0.335,rely=0.5,relwidth=w,relheight=h)

right_btn = tk.Button(master=button_controls,text="right",image=right_arrow,command=move_right)
right_btn.place(relx=0.67,rely=0.5,relwidth=w,relheight=h)

btm_left_btn = tk.Button(master=button_controls,text="backwards left",image=btm_left_arrow,command=move_backward_left)
btm_left_btn.place(rely=0.75,relwidth=w,relheight=h)

backward_btn = tk.Button(master=button_controls,text="backwards",image=down_arrow,command=move_backward)
backward_btn.place(rely=0.75,relx=0.335,relwidth=w,relheight=h)

btm_right_btn = tk.Button(master=button_controls,text="backwards right",image=btm_right_arrow,command=move_backward_right)
btm_right_btn.place(rely=0.75,relx=0.67,relwidth=w,relheight=h)

window.mainloop()