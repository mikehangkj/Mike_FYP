# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time
# import matplotlib.py
import numpy as np

count=0

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

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default="../../../examples/media/people_lying_flat", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--image_dir", default=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\RM_screenshots", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--image_dir", default=r"C:\Users\8051\Pictures\190445A_FYP\Mike_FYP-main\RM_screenshots\2021-07-02-16-42-56.mkv")
    parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
    args = parser.parse_known_args()
    # print(args[0])

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../../models/"
    params["keypoint_scale"] = 0

    # Add others in path?
    # for i in range(0, len(args[1])):
    #     curr_item = args[1][i]
    #     if i != len(args[1])-1: next_item = args[1][i+1]
    #     else: next_item = "1"
    #     if "--" in curr_item and "--" in next_item:
    #         key = curr_item.replace('-','')
    #         if key not in params:  params[key] = "1"
    #     elif "--" in curr_item and "--" not in next_item:
    #         key = curr_item.replace('-','')
    #         if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Read frames on directory
    imagePaths = op.get_images_on_directory(args[0].image_dir);
    start = time.time()
    print(imagePaths)

    # Process and display images
    for imagePath in imagePaths:
        datum = op.Datum()
        imageToProcess = cv2.imread(imagePath)
        datum.cvInputData = imageToProcess
        # print(datum.cvInputData)
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        # print(datum.poseKeypoints)
        # print(datum.cvOutputData)
        # keypoint_1_data = datum.poseKeypoints[0, 1, :]
        # keypoint_8_data = datum.poseKeypoints[0, 8, :]
        # if count==0:
        #     keypoint_xy_data = np.array([keypoint_1_data, keypoint_8_data])
        # else:
        #     keypoint_xy_data=np.insert(keypoint_xy_data,[keypoint_xy_data.shape[0]],[keypoint_1_data, keypoint_8_data],axis=0)
        #     # keypoint_xy_data.append([keypoint_1_data, keypoint_8_data])
        # # print(keypoint_xy_data.shape[0])
        # count+=1
        # print(keypoint_xy_data)
        # print("count=", count)
        # print("Body keypoints: \n" + str(datum.poseKeypoints))

        if not args[0].no_display:
            cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
            key = cv2.waitKey(1) #ms
            if key == 27: break #esc btn

    end = time.time()
    # print(keypoint_xy_data)
    # print(datum.poseKeypoints.shape)
    print(datum.poseKeypoints)
    print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
except Exception as e:
    print(e)
    sys.exit(-1)
