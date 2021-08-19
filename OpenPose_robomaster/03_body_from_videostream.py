# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse

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
            sys.path.append('../../python');
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
    # print(datum)
    # cap = cv2.VideoCapture("../../../examples/media/video.avi")
    cap = cv2.VideoCapture(0)
    # print(cap)
    fps = cap.get(cv2.CAP_PROP_FPS)#get fps
    # print(fps)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) #get width and height of frame
    # print(size)
    framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # print('Total frames in this video: ' + str(framecount))
    videoWriter = cv2.VideoWriter("op720_3.avi", cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), fps, size)
    # print(videoWriter)
    # videoWriter = cv2.VideoWriter(_, cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), fps, size)
    # cv2.VideoWriter()

    while cap.isOpened():
        hasFrame, frame = cap.read()
        # print(cap.read)
        # print(frame)
        if hasFrame:
            # frame = cv2.flip(frame, 90)
            datum.cvInputData = frame
            # print(datum.cvInputData)
            # print(op.VectorDatum)
            # print(op.VectorDatum([datum]))
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            opframe = datum.cvOutputData
            # print(opframe)
            cv2.imshow("main", opframe)
            videoWriter.write(opframe)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(e)
    sys.exit(-1)