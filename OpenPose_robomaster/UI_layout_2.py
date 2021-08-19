import tkinter as tk
from robomaster import robot
from PIL import ImageTk, Image
import cv2
import os
import sys
from time import sleep
from sys import platform

# import tkinter as tk
# from PIL import ImageTk, Image
# import cv2
# from robomaster import robot
# import sys
# import os
# from sys import platform
# from time import sleep

# initialise robot
if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_arm = ep_robot.robotic_arm
    ep_gripper = ep_robot.gripper

    capture = ep_camera.start_video_stream(display=False)

# robomaster chassis controls
x_val = 0.3  # forward distance
y_val = 0.3  # sideways distance
z_val = 15  # distance of turn
xy_s = 1  # speed of forward and sideways m/s
z_s = 90  # speed of turn degrees/s

#number of screenshots
ss = 0

x = 130  # button width
y = 130  # button height

# padding for the button widgets
x_pad = 5
y_pad = 5

#count for op toggle
value=0

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
        print(
            'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
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
    params["disable_blending"] = False  # for black background
    # params["display"] = 0

    # # Add others in path?
    # for i in range(0, len(args[1])):
    #     curr_item = args[1][i]
    #     if i != len(args[1]) - 1:
    #         next_item = args[1][i + 1]
    #     else:
    #         next_item = "1"
    #     if "--" in curr_item and "--" in next_item:
    #         key = curr_item.replace('-', '')
    #         if key not in params:  params[key] = "1"
    #     elif "--" in curr_item and "--" not in next_item:
    #         key = curr_item.replace('-', '')
    #         if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()

except Exception as e:
    print(e)
    sys.exit(-1)

# movement functiions
def move_foward():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=x_val, y=0, z=0, xy_speed=xy_s).wait_for_completed()
    # print("moving forward")

def move_backward():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=xy_s).wait_for_completed()
    # print("moving backwards")

def move_right():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=0, y=y_val, z=0, xy_speed=xy_s).wait_for_completed()
    # print("moving right")

def move_left():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=xy_s).wait_for_completed()
    # print("moving left")

def move_foward_left():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=x_val, y=-y_val, z=0, xy_speed=xy_s).wait_for_completed()
    # print("moving forward and left")

def move_foward_right():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=x_val, y=y_val, z=0, xy_speed=xy_s).wait_for_completed()
    # print("moving forward and right")

def move_backward_left():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=-x_val, y=-y_val, z=0, xy_speed=xy_s).wait_for_completed()
    # print("moving backwards and left")

def move_backward_right():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=-x_val, y=y_val, z=0, xy_speed=xy_s).wait_for_completed()
    # print("moving backwards and right")

def left_turn():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=0, y=0, z=z_val, z_speed=z_s).wait_for_completed()
    # print("left turn")

def right_turn():
    # ep_chassis = ep_robot.chassis
    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_s).wait_for_completed()
    # print("right turn")

# robotic arm movement function
def arm_move_up():
    ep_arm.move(y=20).wait_for_completed()

def arm_move_down():
    ep_arm.move(y=-20).wait_for_completed()

# gripper movement function
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

def stop_program():
    window.destroy()
    ep_camera.stop_video_stream()
    ep_robot.close()

def video_stream():
    # global img
    img = ep_camera.read_cv2_image(strategy="newest")
    sleep(0.1)
    # img = ep_camera.read_cv2_image()
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image, "RGB")
    imgtk = ImageTk.PhotoImage(image=img)
    video.imgtk = imgtk
    video.configure(image=imgtk)
    # video.after(20,video_stream)
    video.after(1, video_stream)

def screenshot(capture, path_output_dir):
    global ss
    print("screenshot")
    print(ss)
    # count=count
    # while capture.isOpened():
    while ss < 1000:
        img2 = ep_camera.read_cv2_image()
        cv2.imwrite(os.path.join(path_output_dir, '%d.png') % ss, img2)
        ss = ss + 1
        break

def button_press(event):
    screenshot(capture, r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\RM_screenshots")
    print("clicked")

# def video_stream_2():
#     # img = ep_camera.read_cv2_image(strategy="newest")
#     # while capture:
#     # _, frame = capture.read()
#     # print(cap.read)
#     # print(frame)
#     if capture:
#         img = ep_camera.read_cv2_image(strategy="newest")
#         sleep(0.1)
#         # frame = cv2.flip(frame, 90)
#         datum.cvInputData = img
#         # print()
#         # cv2image=frame
#         # print(opWrapper.emplaceAndPop)
#         # print(op.VectorDatum([datum]))
#         # opWrapper.emplaceAndPop(frame)
#         # print(opWrapper.emplaceAndPop(op.VectorDatum([datum])))
#         opWrapper.emplaceAndPop(op.VectorDatum([datum]))
#         opframe = datum.cvOutputData
#         # print(opframe)
#         # print(img)
#         cv2image = cv2.cvtColor(opframe, cv2.COLOR_BGR2RGB)
#         # print("cv2 image:",cv2image)
#
#         opframe = Image.fromarray(cv2image, "RGB")
#         # print(img)
#         imgtk = ImageTk.PhotoImage(image=opframe)
#         # print(imgtk)
#         video.imgtk = imgtk
#         # print("running 1")
#         video.configure(image=imgtk)
#         # print("running 2")
#         video.after(1, video_stream_2)
#         # print("running 3")
#         # cv2.imshow("main", opframe)
#         # videoWriter.write(opframe)
#         # if cv2.waitKey(1) & 0xFF == ord('q'):
#         #     break
#     else:
#     #     # print("breaking")
#     #     # break
#         capture.release()
#         cv2.destroyAllWindows()

def video_stream():
    img = ep_camera.read_cv2_image(strategy="newest")
    sleep(0.1)
    if value==1:
        datum.cvInputData = img
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        opframe = datum.cvOutputData
        cv2image = cv2.cvtColor(opframe, cv2.COLOR_BGR2RGB)
        # cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # print("cv2 image:",cv2image)

        opframe = Image.fromarray(cv2image, "RGB")
        # img = Image.fromarray(cv2image, "RGB")
        # print(img)
        imgtk = ImageTk.PhotoImage(image=opframe)
        # imgtk = ImageTk.PhotoImage(image=img)

        # print(imgtk)
        video.imgtk = imgtk
        # print("running 1")
        video.configure(image=imgtk)
        # print("running 2")
        video.after(1, video_stream)
    else:
        # img = ep_camera.read_cv2_image()
        cv2image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img=Image.fromarray(cv2image,"RGB")
        imgtk=ImageTk.PhotoImage(image=img)
        video.imgtk=imgtk
        video.configure(image=imgtk)
        # video.after(20,video_stream)
        video.after(1,video_stream)

def button_pressed():
    global value
    value += 1
    print("toggle op")
    if value == 2:
        print("reset value")
        value=0
    else:
        pass

window = tk.Tk()
window.title("RoboMaster UI")

window.geometry("1920x1280")

# window.columnconfigure([0,1], minsize=150,weight=1)
# window.rowconfigure(0,minsize=100,weight=1)
window.columnconfigure([0, 1], weight=1)
window.rowconfigure(0, weight=1)

# display window
# photo=tk.PhotoImage(file="frog.png")
# ,image=photo
display = tk.Frame(master=window, bg="black", width=100, height=30)
# display.grid(row=0,column=0,padx=5,pady=5)
display.place(rely=0.05, relx=0.025, relwidth=0.5, relheight=0.6)

upward = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\fyp_pics\upward.png")
downward = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\fyp_pics\downward.png")
forward = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\fyp_pics\forward.png")
backward = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\fyp_pics\backward.png")

video = tk.Label(display,bg="black")
video.place(relwidth=1, relheight=0.9)

button = tk.Button(display, text="click to start stream", command=video_stream)
button.place(rely=0.9, relwidth=1, relheight=0.05)

button2 = tk.Button(display, text="click to toggle openpose", command=button_pressed)
button2.place(rely=0.95, relwidth=1, relheight=0.05)

gripper_func_display = tk.Frame(master=window, width=100, height=30)
gripper_func_display.place(rely=0.65, relx=0.025, relwidth=0.5, relheight=0.3)

# gripper_func=tk.Label(master=gripper_func_display,text="gripper functions",relief="ridge",font=20)
# gripper_func.place(relx=0.5,relwidth=0.5,relheight=0.1)

open_gripper = tk.Button(gripper_func_display, text="open gripper", font=20, command=gripper_open)
open_gripper.place(relx=0.5, rely=0.1, relwidth=0.25, relheight=0.3)

close_gripper = tk.Button(gripper_func_display, text="close gripper", font=20, command=gripper_close)
close_gripper.place(relx=0.75, rely=0.1, relwidth=0.25, relheight=0.3)

arm_func = tk.Label(master=gripper_func_display, text="robotic arm functions", font=20, relief="ridge")
arm_func.place(rely=0.1, relwidth=0.5, relheight=0.3)

arm_up = tk.Button(master=gripper_func_display, image=upward, font=20, command=arm_move_up)
arm_up.place(rely=0.4, relwidth=0.25, relheight=0.6)

arm_down = tk.Button(master=gripper_func_display, image=downward, font=20, command=arm_move_down)
arm_down.place(rely=0.4, relx=0.25, relwidth=0.25, relheight=0.6)

gripper_forward = tk.Button(master=gripper_func_display, image=forward, font=20, command=gripper_move_fw)
gripper_forward.place(rely=0.4, relx=0.75, relwidth=0.25, relheight=0.6)

gripper_backward = tk.Button(master=gripper_func_display, image=backward, font=20, command=gripper_move_bw)
gripper_backward.place(rely=0.4, relx=0.5, relwidth=0.25, relheight=0.6)

up_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\up_arrow.png")
down_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\down_arrow.png")
left_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\left_arrow.png")
right_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\right_arrow.png")
top_right_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\top_right_arrow.png")
top_left_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\top_left_arrow.png")
btm_right_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\btm_right_arrow.png")
btm_left_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\btm_left_arrow.png")
camera_pic = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\camera_pic.png")
left_turn_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\back_arrow.png")
right_turn_arrow = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\redo_arrow.png")
power_button = tk.PhotoImage(file=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\arrow_pics_2\power_button.png")

# gimbal controls
button_controls = tk.Frame(master=window)
button_controls.grid(row=0, column=1)
# gripper_btn = tk.Button(master=button_controls,image=gripper_pic,width=x,height=y).grid(row=0,column=1,sticky="nsew")

left_turn_btn = tk.Button(master=button_controls, image=left_turn_arrow, width=x, height=y, command=left_turn)
left_turn_btn.grid(row=0, column=0, sticky="nsew", padx=x_pad, pady=y_pad)

right_turn_btn = tk.Button(master=button_controls, image=right_turn_arrow, width=x, height=y, command=right_turn)
right_turn_btn.grid(row=0, column=2, sticky="nsew", padx=x_pad, pady=y_pad)

up_btn = tk.Button(master=button_controls, image=up_arrow, width=x, height=y, command=move_foward)
up_btn.grid(row=1, column=1, sticky="nsew", padx=x_pad, pady=y_pad)

down_btn = tk.Button(master=button_controls, image=down_arrow, width=x, height=y, command=move_backward)
down_btn.grid(row=3, column=1, sticky="nsew", padx=x_pad, pady=y_pad)

right_btn = tk.Button(master=button_controls, image=right_arrow, width=x, height=y, command=move_right)
right_btn.grid(row=2, column=2, sticky="nsew", padx=x_pad, pady=y_pad)

left_btn = tk.Button(master=button_controls, image=left_arrow, width=x, height=y, command=move_left)
left_btn.grid(row=2, column=0, sticky="nsew", padx=x_pad, pady=y_pad)

top_right_btn = tk.Button(master=button_controls, image=top_right_arrow, width=x, height=y, command=move_foward_right)
top_right_btn.grid(row=1, column=2, sticky="nsew", padx=x_pad, pady=y_pad)

top_left_btn = tk.Button(master=button_controls, image=top_left_arrow, width=x, height=y, command=move_foward_left)
top_left_btn.grid(row=1, column=0, sticky="nsew", padx=x_pad, pady=y_pad)

btm_left_btn = tk.Button(master=button_controls, image=btm_left_arrow, width=x, height=y, command=move_backward_left)
btm_left_btn.grid(row=3, column=0, sticky="nsew", padx=x_pad, pady=y_pad)

btm_right_btn = tk.Button(master=button_controls, image=btm_right_arrow, width=x, height=y, command=move_backward_right)
btm_right_btn.grid(row=3, column=2, sticky="nsew", padx=x_pad, pady=y_pad)

# u_turn_btn = tk.Button(master=button_controls,image=u_turn_arrow,width=x,height=y,command=move_anti_cw)
# u_turn_btn.grid(row=1,column=1)

stop_btn = tk.Button(master=button_controls, image=power_button, width=x, height=y, command=stop_program)
stop_btn.grid(row=2, column=1, padx=x_pad, pady=y_pad)

camera_btn = tk.Button(master=button_controls, image=camera_pic, width=x, height=y)
camera_btn.grid(row=0, column=1, padx=x_pad, pady=y_pad)
camera_btn.bind("<Button-1>", button_press)
# width=350,height=31

# Label=tk.Label(master=button_controls,text="arm controls",width=5,height=5)
# Label.grid(row=0,column=4)

window.mainloop()
