import cv2
import robomaster
from robomaster import robot
from robomaster import vision
from time import sleep

# x_val = 0.5
# y_val = 0.55
x_val = 0.1
y_val = 0.106
z_val = 90
xy_spd = 1
z_spd = 50
w_val=0.138

class MarkerInfo:

    def __init__(self, x, y, w, h, info):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def text(self):
        return self._info

markers = []

def on_detect_marker(marker_info):
    global x, y, w, h, info
    number = len(marker_info)
    # print(number)
    # print("markers", markers)
    markers.clear()
    # print("markers",markers)
    for i in range(0, number):
        x, y, w, h, info = marker_info[i]
        markers.append(MarkerInfo(x, y, w, h, info))
        # print(type(markers))
        # print("x",x)
        # print("y",y)
        # print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
        # print("markerinfo",marker_info)

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis

    ep_camera.start_video_stream(display=False)
    sleep(3)
    result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)

    # print("1")
    # ep_chassis.move(x=x_val, y=0, z=0, xy_speed=xy_spd).wait_for_completed()

    # for i in range(0,20):
    #     img = ep_camera.read_cv2_image(strategy="newest")
    #     # img = ep_camera.read_cv2_image(strategy="newest",timeout=0.5)
    #     for j in range(0, len(markers)):
    #         cv2.rectangle(img, markers[j].pt1, markers[j].pt2, (255, 255, 255))
    #         cv2.putText(img, markers[j].text, markers[j].center, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    #     cv2.imshow("Markers", img)
    #     cv2.waitKey(1)
    # cv2.destroyAllWindows()

    # print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
    # print("marker",info)

    # while True:
    #     if w>0.13 and info==1:
    #         ep_chassis.move(x=-0.25, y=0, z=0, xy_speed=xy_spd).wait_for_completed()
    #         print("move backward")
    #         break
    #     else:
    #         ep_chassis.move(x=0.25, y=0, z=0, xy_speed=xy_spd).wait_for_completed()
    #         print("move forward")

    # if (w>0.13 and info=="1"):
    #     ep_chassis.move(x=-0.25, y=0, z=0, xy_speed=xy_spd).wait_for_completed()
    #     print("move backward")
    #     print(info)
    # else:
    #     ep_chassis.move(x=0.25, y=0, z=0, xy_speed=xy_spd).wait_for_completed()
    #     print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))

    while True:
        try:
            img = ep_camera.read_cv2_image(strategy="newest")
            # sleep(0.1)
            cv2.imshow("Markers", img)
            cv2.waitKey(1)
            if w>w_val:
            # if x>0.49 and x<0.51:
                ep_chassis.move(x=0, y=0, z=0, xy_speed=xy_spd).wait_for_completed()
                sleep(1)
                print("stop")
                # print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}
                # if x < 0.495:
                #     print("moving left")
                #     print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
                #     ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=xy_spd).wait_for_completed()
                #     # sleep(0.1)
                # elif x > 0.505:
                #     print("moving right")
                #     print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
                #     ep_chassis.move(x=0, y=y_val, z=0, xy_speed=xy_spd).wait_for_completed()


                if w>w_val and info=="1":
                    print("info:", info + " turn left")
                    # print("turn left")
                    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_spd).wait_for_completed()
                elif w>w_val and info=="2":
                    print("info:", info + " turn left")
                    # print("info:", info)
                    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_spd).wait_for_completed()
                elif w>w_val and info=="3":
                    print("info:", info + " turn left")
                    # print("info:",info)
                    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_spd).wait_for_completed()
                elif w>w_val and info == "4":
                    print("info:", info + " turn left")
                    # print("info:",info)
                    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_spd).wait_for_completed()

            # if w>0.13 and info=="4":
            #     break
            else:
                if x < 0.485:
                    print("moving left")
                    print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
                    ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=xy_spd).wait_for_completed()
                    # sleep(0.1)
                if x > 0.515:
                    print("moving right")
                    print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
                    ep_chassis.move(x=0, y=y_val, z=0, xy_speed=xy_spd).wait_for_completed()

                else:
                    ep_chassis.move(x=0.25, y=0, z=0, xy_speed=xy_spd).wait_for_completed()
                    print("move forward")
                    print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
        except:
            print("marker is not detected")
            continue

    # print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))

    result = ep_vision.unsub_detect_info(name="marker")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()