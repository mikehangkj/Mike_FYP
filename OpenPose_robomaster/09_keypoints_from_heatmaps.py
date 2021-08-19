# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

# count=0

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
    # parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000294.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000241.jpg",help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--image_path", default="../../../examples/media/person_lying_down.jpg",help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--image_path", default="../../../examples/media/woman_lying_sideways.jpg",help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--image_path", default="../../../examples/media/people_lying_down/1.jpg" ,help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--image_path", default="../../../examples/media/people_lying_flat/images.jpg",help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")#15
    # parser.add_argument("--image_path", default="../../../examples/media/people_lying_flat/images (1).jpg",help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")#9
    parser.add_argument("--image_path", default="../../../examples/media/people_lying_flat/download.jpg",help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--image_path", default="../../../examples/media/download.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()
    # print(args[0])

    # Load image
    imageToProcess = cv2.imread(args[0].image_path)
    # print("1")

    def get_sample_heatmaps():
        # These parameters are globally set. You need to unset variables set here if you have a new OpenPose object. See *
        params = dict()
        params["model_folder"] = "../../../models/"
        params["heatmaps_add_parts"] = True
        params["heatmaps_add_bkg"] = True
        params["heatmaps_add_PAFs"] = True
        params["heatmaps_scale"] = 3
        params["upsampling_ratio"] = 1
        params["body"] = 1
        params["model_pose"]="BODY_25"
        params["keypoint_scale"]=3

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Image and get heatmap
        datum = op.Datum()
        # print(args[0])
        # print("2")
        imageToProcess = cv2.imread(args[0].image_path)
        datum.cvInputData = imageToProcess
        # print(datum.cvInputData)

        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        poseHeatMaps = datum.poseHeatMaps.copy()
        opWrapper.stop()

        # print(poseHeatMaps)
        return poseHeatMaps

    # Get Heatmap
    poseHeatMaps = get_sample_heatmaps()
    # print(poseHeatMaps)

    # Starting OpenPose
    params = dict()
    params["model_folder"] = "../../../models/"
    params["body"] = 2  # Disable OP Network
    params["upsampling_ratio"] = 0 # * Unset this variable

    # print(params)
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Pass Heatmap and Run OP
    datum = op.Datum()
    # print("1")
    datum.cvInputData = imageToProcess
    # print(poseHeatMaps)
    # print("2")
    datum.poseNetOutput = poseHeatMaps
    # print("3")
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))
    # print("4")
    # print(datum.poseKeypoints)
    # keypoint_0_data = datum.poseKeypoints[0, 0, :] #error here
    keypoint_1_data = datum.poseKeypoints[0, 1, :]
    keypoint_8_data = datum.poseKeypoints[0, 8, :]

    #plot graph
    x1=[keypoint_1_data[0],keypoint_8_data[0]]
    y1=[keypoint_1_data[1],keypoint_8_data[1]]

    plt.plot(x1,y1, label="kp1")
    # x8 = keypoint_8_data[0]
    # y8 = keypoint_8_data[1]
    #
    # plt.plot(x8, y8, label="kp8")

    # plt.xlabel('x - axis')
    # naming the y axis
    # plt.ylabel('y - axis')
    # giving a title to my graph
    # plt.title('Two lines on same graph!')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    # plt.show()

    # Display Image
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    # print(type(datum.poseKeypoints))
    # print("keypoint 0: \n", keypoint_0_data)
    print("keypoint 1: \n", keypoint_1_data)
    print("keypoint 8: \n", keypoint_8_data)
    print("variance:\n",keypoint_1_data[1]-keypoint_8_data[1])

    # if keypoint_1_data[0] > keypoint_8_data[0]:
    #     print("person feet facing left")
    #     if keypoint_1_data[1] > keypoint_8_data[1]:
    #         if keypoint_1_data[1]-keypoint_8_data[1] > 0.15:
    #             print("person is ok")
    #         else:
    #             print("on their back")
    #     else:
    #         if keypoint_8_data[1]-keypoint_1_data[1] > 0.15:
    #             print(keypoint_8_data[1]-keypoint_1_data[1])
    #             print("person is ok")
    #         else:
    #             print(keypoint_8_data[1] - keypoint_1_data[1])
    #             print("face down")
    # else:
    #     pass
    # if keypoint_8_data[0] > keypoint_1_data[0]:
    #     print("person feet facing right")
    #     if keypoint_1_data[1]-keypoint_8_data[1]>1.5:
    #         print("not lying down")

    # if keypoint_1_data[1] > keypoint_8_data[1]:
    #     if keypoint_1_data[1]-keypoint_8_data[1] < 0.12:
    #         print(keypoint_1_data[1]-keypoint_8_data[1])
    #         print("person is lying down")
    #     elif keypoint_1_data[1]-keypoint_8_data[1] >= 0.12:
    #         print(keypoint_1_data[1]-keypoint_8_data[1])
    #         print("person is not lying down")
    # else:
    #     pass
    #
    # if keypoint_8_data[1] > keypoint_1_data[1]:
    #     if keypoint_8_data[1] - keypoint_1_data[1] < 0.12:
    #         print(keypoint_8_data[1] - keypoint_1_data[1])
    #         print("person is lying down")
    #     elif keypoint_8_data[1] - keypoint_1_data[1] >= 0.12:
    #         print(keypoint_8_data[1] - keypoint_1_data[1])
    #         print("person is not lying down")
    # else:
    #     pass

    ax = plt.gca()  # get the axis
    ax.invert_yaxis() #invert y axis
    ax.xaxis.tick_top() #flip x axis up
    cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
    plt.legend(bbox_to_anchor=(1, 1), loc="upper left", borderaxespad=0.1)
    plt.show()
    cv2.waitKey(0)

except Exception as e:
    print(e)
    sys.exit(-1)
