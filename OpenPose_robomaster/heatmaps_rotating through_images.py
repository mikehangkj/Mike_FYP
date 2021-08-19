import sys
import cv2
import os
from sys import platform
import argparse
import time
import matplotlib.pyplot as plt
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
            sys.path.append('../../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    parser = argparse.ArgumentParser()
    # parser.add_argument("--image_path", default="../../../examples/media/people_lying_flat/images (1).jpg",help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--image_dir", default="../../../examples/media/people_lying_flat",help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
    args = parser.parse_known_args()

    imagePaths = op.get_images_on_directory(args[0].image_dir);

    def get_sample_heatmaps():
        global imageToProcess
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
        # print("1")
        imageToProcess = cv2.imread(imagePath)
        # print("2")
        datum.cvInputData = imageToProcess
        print(opWrapper.emplaceAndPop(op.VectorDatum([datum])))
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        poseHeatMaps = datum.poseHeatMaps.copy()
        # print("1", datum.poseHeatMaps)
        # print("2",poseHeatMaps)
        opWrapper.stop()
        return poseHeatMaps

    # poseHeatMaps = get_sample_heatmaps()

    params=dict()
    params["model_folder"] = "../../../models/"
    # params["body"] = 2  # Disable OP Network
    params["upsampling_ratio"] = 0 # * Unset this variable
    params["keypoint_scale"] = 3

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # params = dict()
    # params["model_folder"] = "../../../models/"
    # params["heatmaps_add_parts"] = True
    # params["heatmaps_add_bkg"] = True
    # params["heatmaps_add_PAFs"] = True
    # params["heatmaps_scale"] = 3
    # params["upsampling_ratio"] = 1
    # params["body"] = 1
    # params["model_pose"] = "BODY_25"
    # params["keypoint_scale"] = 3
    #
    # opWrapper = op.WrapperPython()
    # opWrapper.configure(params)
    # opWrapper.start()

    start = time.time()

    for imagePath in imagePaths:
        datum = op.Datum()
        # imageToProcess = cv2.imread(imagePath)
        get_sample_heatmaps()
        datum.cvInputData = imageToProcess
        # datum.poseNetOutput = datum.poseHeatMaps
        # print(datum.cvInputData)
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        # print(datum.poseHeatMaps)

        # datum.poseNetOutput = datum.poseHeatMaps.copy()

        # opWrapper.emplaceAndPop(op.VectorDatum([datum]))

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

        x1 = [keypoint_1_data[0], keypoint_8_data[0]]
        y1 = [keypoint_1_data[1], keypoint_8_data[1]]

        # #plot x data on graph
        plt.plot(x1,y1,label=count)
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.title("x-data for kps 1 and 8")
        print("image =", count)
        print("variance:\n", keypoint_1_data[1] - keypoint_8_data[1])

        if not args[0].no_display:
            cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
            key = cv2.waitKey(1)  # ms
            if key == 27: break  # esc btn

    end = time.time()
    ax = plt.gca()  # get the axis
    ax.invert_yaxis() #invert y axis
    ax.xaxis.tick_top() #flip x axis up

    plt.legend(bbox_to_anchor=(1, 1),loc="upper left",borderaxespad=0.1)
    plt.show()
    # print(keypoint_xy_data)
    # print(datum.poseKeypoints.shape)
    print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")

except Exception as e:
    print(e)
    sys.exit(-1)