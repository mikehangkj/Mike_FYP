import tkinter as tk
from PIL import ImageTk, Image
import cv2
from robomaster import robot
import sys
import os
from sys import platform
from time import sleep

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_camera = ep_robot.camera

capture = ep_camera.start_video_stream(display=False)
    # print(capture)


# print(capture)

# def video_stream():
#     global cv2image
#
#     img = ep_camera.read_cv2_image(strategy="newest")
#
#     #
#     cv2image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#
#     img=Image.fromarray(cv2image,"RGB")
#
#
#     imgtk=ImageTk.PhotoImage(image=img)
#     main_label.imgtk=imgtk
#     main_label.configure(image=imgtk)
#     main_label.after(1,video_stream)
#
#

# print("capture:",capture)

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
    # cv2image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    # cap = cv2.VideoCapture("../../../examples/media/video.avi")
    # cap = cv2.VideoCapture(0)
    # fps = cap.get(cv2.CAP_PROP_FPS) #get fps
    # print(fps)
    # size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) #get width and height of frame
    # print(size)
    # framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # print('Total frames in this video: ' + str(framecount))
    # videoWriter = cv2.VideoWriter("op720_1.avi", cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), 30, (1300,750))

    # videoWriter = cv2.VideoWriter(_, cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), fps, size)
    # cv2.VideoWriter()

except Exception as e:
    print(e)
    sys.exit(-1)

def video_stream_2():
    # while capture:
    # _, frame = capture.read()
    # print(cap.read)
    # print(frame)
    # if capture:
    img = ep_camera.read_cv2_image(strategy="newest")
    sleep(0.1)
    # frame = cv2.flip(frame, 90)
    datum.cvInputData = img
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))
    opframe = datum.cvOutputData
    # print()
    # cv2image=frame
    # print(opWrapper.emplaceAndPop)
    # print(op.VectorDatum([datum]))
    # opWrapper.emplaceAndPop(frame)
    # print(opWrapper.emplaceAndPop(op.VectorDatum([datum])))

    # img = datum.cvOutputData
    # print(opframe)
    # print(img)
    cv2image = cv2.cvtColor(opframe, cv2.COLOR_BGR2RGB)
    # cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print("cv2 image:",cv2image)

    opframe = Image.fromarray(cv2image, "RGB")
    # img = Image.fromarray(cv2image, "RGB")
    # print(img)
    imgtk = ImageTk.PhotoImage(image=opframe)
    # imgtk = ImageTk.PhotoImage(image=img)

    # print(imgtk)
    main_label.imgtk = imgtk
    # print("running 1")
    main_label.configure(image=imgtk)
    # print("running 2")
    main_label.after(1, video_stream_2)
    # print("running 3")
    # cv2.imshow("main", opframe)
    # videoWriter.write(opframe)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    # else:
    #     # print("breaking")
    #     # break
    #     capture.release()
    #     cv2.destroyAllWindows()
    poseModel = op.PoseModel.BODY_25
    print(op.getPoseBodyPartMapping(poseModel))
    print(op.getPoseNumberBodyParts(poseModel))
    print(op.getPosePartPairs(poseModel))
    print(op.getPoseMapIndex(poseModel))

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
        main_label.imgtk = imgtk
        # print("running 1")
        main_label.configure(image=imgtk)
        # print("running 2")
        main_label.after(1, video_stream)
    else:
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
