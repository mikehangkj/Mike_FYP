# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time
import matplotlib.pyplot as plt
import numpy as np

count=0
average_v=0
total_v=0

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
    params["keypoint_scale"] = 3
    # params["heatmaps_add_parts"] = True
    # params["heatmaps_add_bkg"] = True
    # params["heatmaps_add_PAFs"] = True
    # params["heatmaps_scale"] = 3
    # params["upsampling_ratio"] = 1
    # params["body"] = 1
    # params["model_pose"] = "BODY_25"
    # params["keypoint_scale"] = 3

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
    # print(imagePaths)

    # Process and display images
    for imagePath in imagePaths: #run through the images in image path
        datum = op.Datum()
        imageToProcess = cv2.imread(imagePath)
        datum.cvInputData = imageToProcess
        # datum.poseNetOutput = datum.poseHeatMaps.copy()
        # print(datum.cvInputData)
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        # print(opWrapper.emplaceAndPop(op.VectorDatum([datum])))
        # poseHeatMaps = datum.poseHeatMaps.copy()

        # def input_heatmap_data():
        #     opWrapper.start()
        #     datum = op.Datum()
        #     imageToProcess = cv2.imread(imagePath)
        #     datum.cvInputData = imageToProcess
        #     datum.poseNetOutput = poseHeatMaps
        #
        #     print(type(poseHeatMaps))
        #     print(poseHeatMaps.shape)
        #     opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        #     print("2",opWrapper.emplaceAndPop(op.VectorDatum([datum])))
        #     # opWrapper.stop()
        #
        # if opWrapper.emplaceAndPop(op.VectorDatum([datum])) == True:
        #     print("1")
        #     poseHeatMaps = datum.poseHeatMaps.copy()
        #     print("2")
        #     input_heatmap_data()
        # else:
        #     pass
            # print(poseHeatMaps)

        # print(opWrapper.emplaceAndPop(op.VectorDatum([datum])))
        # poseHeatMaps = datum.poseHeatMaps.copy()
        # datum.poseNetOutput = poseHeatMaps
        # print(poseHeatMaps)
        # opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        # print(datum.poseKeypoints)
        # print(datum.cvOutputData)
        # kp_0_data = datum.poseKeypoints[]
        # keypoint_0_data = datum.poseKeypoints[0, 0, :]
        keypoint_1_data = datum.poseKeypoints[0, 1, :]
        keypoint_8_data = datum.poseKeypoints[0, 8, :]

        count+=1
        if count==1:
            # kp_0_data = np.array([keypoint_0_data])
            kp_1_data = np.array([keypoint_1_data])
            kp_8_data = np.array([keypoint_8_data])
        else:
            # kp_0_data = np.insert(kp_0_data, [kp_0_data.shape[0]],[keypoint_0_data],axis=0)
            kp_1_data = np.insert(kp_1_data, [kp_1_data.shape[0]],[keypoint_1_data],axis=0)
            kp_8_data = np.insert(kp_8_data, [kp_8_data.shape[0]],[keypoint_8_data],axis=0)
        # if count==0:
        #     keypoint_xy_data = np.array([keypoint_1_data, keypoint_8_data])
        # else:
        #     keypoint_xy_data=np.insert(keypoint_xy_data,[keypoint_xy_data.shape[0]],[keypoint_1_data, keypoint_8_data],axis=0)
        #     # keypoint_xy_data.append([keypoint_1_data, keypoint_8_data])
        # # print(keypoint_xy_data.shape[0])
        # x1 = [keypoint_0_data[0],keypoint_1_data[0], keypoint_8_data[0]]
        # y1 = [keypoint_0_data[1],keypoint_1_data[1], keypoint_8_data[1]]
        x1 = [keypoint_1_data[0], keypoint_8_data[0]]
        y1 = [keypoint_1_data[1], keypoint_8_data[1]]

        # #plot x data on graph

        # plt.plot(x1,y1, label="img %d"%count)
        plt.plot(x1,y1,label=count)
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.title("x-data for kps 1 and 8")

        # count+=1
        print("image =", count)
        # print("key point 0: \n", kp_0_data)
        # print("Body keypoints: \n" + str(datum.poseKeypoints))
        # print("key point 1: \n", kp_1_data)
        # print("key point 8: \n", kp_8_data)
        variance = keypoint_1_data[1] - keypoint_8_data[1]
        print("variance:\n", variance)
        total_v=total_v+ abs(variance)
        print("total",total_v)
        # average_v=(average_v+variance)/count
        # print(average_v)

        # if kp_8_data[1]-kp_1_data[1]<0.15:
        #     print("person is lying down")
        #
        if keypoint_1_data[1] > keypoint_8_data[1]:
            if keypoint_1_data[1] - keypoint_8_data[1] < 0.13:
                # print(keypoint_1_data[1] - keypoint_8_data[1])
                print("person is lying down")
            elif keypoint_1_data[1] - keypoint_8_data[1] >= 0.13:
                # print(keypoint_1_data[1] - keypoint_8_data[1])
                print("person is not lying down")
        else:
            pass

        if keypoint_8_data[1] > keypoint_1_data[1]:
            if keypoint_8_data[1] - keypoint_1_data[1] < 0.13:
                # print(keypoint_8_data[1] - keypoint_1_data[1])
                print("person is lying down")
            elif keypoint_8_data[1] - keypoint_1_data[1] >= 0.13:
                # print(keypoint_8_data[1] - keypoint_1_data[1])
                print("person is not lying down")
        else:
            pass
        # if keypoint_8_data[1]==keypoint_1_data[1]:
        #     print("kp 8 and kp 1 is 0")

        # if keypoint_1_data[0] > keypoint_8_data[0]:
        #     # print("person feet facing left")
        #     if keypoint_1_data[1] < keypoint_8_data[1]:
        #         print("ffl on their back")
        #     else:
        #         print("ffl face down")
        # else:
        #     pass
        # if keypoint_8_data[0] > keypoint_1_data[0]:
        #     # print("person feet facing right")
        #     if keypoint_1_data[1] < keypoint_8_data[1]:
        #         print("ffr on their back")
        #     else:
        #         print("ffr face down")

        # print("Body keypoints: \n" + str(datum.poseKeypoints))

        if not args[0].no_display:
            cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
            key = cv2.waitKey(1) #ms
            if key == 27: break #esc btn
    #
    # #plot x data on graph
    # x1 = [ keypoint_1_data[0], keypoint_8_data[0]]
    # plt.plot(x1, label="kp1")

    end = time.time()
    ax = plt.gca()  # get the axis
    ax.invert_yaxis() #invert y axis
    ax.xaxis.tick_top() #flip x axis up
    average_v=(total_v/count)
    print("average variance:",average_v)

    plt.legend(bbox_to_anchor=(1, 1),loc="upper left",borderaxespad=0.1)
    plt.show()
    # print(keypoint_xy_data)

    print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
except Exception as e:
    print(e)
    sys.exit(-1)
