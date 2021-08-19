import tkinter as tk
from PIL import ImageTk, Image
import cv2
from robomaster import robot
import sys
import os
from sys import platform
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACceb9987210600c24e369f06afc4cdd9f"
# Your Auth Token from twilio.com/console
auth_token  = "c2707e45ac641a03ac69ab508b7f3ade"

client = Client(account_sid, auth_token)

count=0
T=0.05 #tolerance
sms=0

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_camera = ep_robot.camera
    capture = ep_camera.start_video_stream(display=False)
    print(capture)

def play_audio():
    print("playing audio")
    # ep_robot.play_audio(filename="output6.wav").wait_for_completed()
    ep_robot.play_audio(filename="gtts2.wav").wait_for_completed()

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
            # op.Datum.
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
            # from openpose import openpose_python as op1
            # import openpose
            # openpose.
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
    # params["fullscreen"] = True
    # params["number_people_max"] = 2
    params["disable_blending"] = False   # for black background
    params["keypoint_scale"] = 3
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
    # cap = cv2.VideoCapture("../../../examples/media/video.avi")
    # cap = cv2.VideoCapture(0)
    # fps = cap.get(cv2.CAP_PROP_FPS) #get fps
    # print(fps)
    # size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) #get width and height of frame
    # print(size)
    # framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # print('Total frames in this video: ' + str(framecount))
    videoWriter = cv2.VideoWriter("op720_1.avi", cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), 30, (1300, 750))
    # videoWriter = cv2.VideoWriter("op720_1.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (1300, 750))
    # videoWriter = cv2.VideoWriter("op720_1.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1300, 750))
    # videoWriter = cv2.VideoWriter(_, cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), fps, size)
    # cv2.VideoWriter()

    while capture:
        # _, frame = capture.read()
        # print(cap.read)
        # print(frame)
        try:
            img = ep_camera.read_cv2_image(strategy="newest")
            sleep(0.1)
            # frame = cv2.flip(frame, 90)
            datum.cvInputData = img
            # print()
            # cv2image=frame
            # print("emplace and pop:",opWrapper.emplaceAndPop)
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            # print("poggers:",opWrapper.emplaceAndPop(op.VectorDatum([datum])))
            opframe = datum.cvOutputData
            # print("datum posekeypoints:\n",datum.poseKeypoints)

            if datum.poseKeypoints.any()!=None:
                # print(str(datum.poseKeypoints))
                keypoint_1_data = datum.poseKeypoints[0, 1, :]
                keypoint_8_data = datum.poseKeypoints[0, 8, :]

                # print(type(keypoint_1_data[1]))

                print("keypoint 1 data",keypoint_1_data)
                print("keypoint 8 data",keypoint_8_data)

                count += 1
                if count == 1:
                    # kp_0_data = np.array([keypoint_0_data])
                    kp_1_data = np.array([keypoint_1_data])
                    kp_8_data = np.array([keypoint_8_data])
                else:
                    # kp_0_data = np.insert(kp_0_data, [kp_0_data.shape[0]],[keypoint_0_data],axis=0)
                    kp_1_data = np.insert(kp_1_data, [kp_1_data.shape[0]], [keypoint_1_data], axis=0)
                    kp_8_data = np.insert(kp_8_data, [kp_8_data.shape[0]], [keypoint_8_data], axis=0)

                # print("keypoint 1 data:",keypoint_1_data)
                # print("keypoint 8 data:",keypoint_8_data)

                if keypoint_1_data[1] > keypoint_8_data[1]:
                    if keypoint_1_data[1] - keypoint_8_data[1] < T:
                        # print(keypoint_1_data[1] - keypoint_8_data[1])
                        print("person is lying down")
                        sms+=1

                        while sms==20:
                            message = client.messages.create(to="+6596930075",from_="+1 818 485 4907",body="the person is lying down!")
                            play_audio()
                            sms=0

                    elif keypoint_1_data[1] - keypoint_8_data[1] >= T:
                        # print(keypoint_1_data[1] - keypoint_8_data[1])
                        print("person is not lying down")
                else:
                    pass

                if keypoint_8_data[1] > keypoint_1_data[1]:
                    if keypoint_8_data[1] - keypoint_1_data[1] < T:
                        # print(keypoint_8_data[1] - keypoint_1_data[1])
                        print("person is lying down")
                        sms+=1

                        while sms==20:
                            message = client.messages.create(to="+6596930075",from_="+1 818 485 4907",body="the person is lying down!")
                            play_audio()
                            sms=0

                    elif keypoint_8_data[1] - keypoint_1_data[1] >= T:
                        # print(keypoint_8_data[1] - keypoint_1_data[1])
                        print("person is not lying down")
                else:
                    pass
            else:
                pass

            # print(datum.poseKeypoints)

            # opWrapper.emplaceAndPop(op.VectorDatum([datum]))


            # keypoint_1_data = datum.poseKeypoints[0, 1, :]
            # keypoint_8_data = datum.poseKeypoints[0, 8, :]
            # print(keypoint_1_data)

            # print(opframe)
            # print(img)

            cv2.imshow("main", opframe)
            # print(datum.poseKeypoints)
            videoWriter.write(opframe)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # else:
        #     print("breaking")
        #     break

        except:
            print("no object detected")
            continue

    capture.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(e)
    sys.exit(-1)