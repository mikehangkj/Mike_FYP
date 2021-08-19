import cv2
import robomaster
from robomaster import robot
from robomaster import vision
from time import sleep

#instead of using w to see the distance we can use y instead

# x_val = 0.5
# y_val = 0.55
# x_val = 0.25
x_val = 0.1
y_val = 0.106
# y_val = 0.265

z_val = 90
xy_spd = 1
z_spd = 50
# w_val=0.138
yy=0.69375 #0.5m

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

    while True:
        img = ep_camera.read_cv2_image(strategy="newest")
        # sleep(0.1)
        cv2.imshow("Markers", img)
        cv2.waitKey(1)

        # if

    result = ep_vision.unsub_detect_info(name="marker")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()