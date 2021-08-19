import cv2
import robomaster
from robomaster import robot
from robomaster import vision
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# x_val = 0.5
# y_val = 0.55
# x_val = 0.25
x_val = 0.3
y_val = 0.106
# y_val = 0.265

z_val = 90
xy_spd = 1
z_spd = 50
# w_val=0.138
yy=0.69375 #0.5m

m=0
count=0
x_data=0
y_data=0
x1=[]
y1=[]

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

# def animate(i):
#     global x1, y1
#
#
#     print("m:", m)
#     print("x data:", x_data)
#     print("y data",y_data)
#     print("y1:",y1)
#     print("x1:",x1)
#     # for m in x1:
#     if x_data != x1[m-1]:
#         x1.append(x_data)
#         y1.append(y_data)
#         # print("x1",x1)
#         # print("y1",y1)
#         plt.cla()
#         plt.plot(x1,y1)
#         plt.tight_layout()
#     if y_data != y1[m-1]:
#         x1.append(x_data)
#         y1.append(y_data)
#         # print("x1",x1)
#         # print("y1",y1)
#         plt.cla()
#         plt.plot(x1, y1)
#         plt.tight_layout()
#     else:
#         plt.cla()
#         plt.plot(x1, y1)
#         plt.tight_layout()
#         print("plotted")



def animate(i):
    plt.cla()
    plt.plot(x1, y1)
    plt.tight_layout()
    # print("plotted")


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis

    ep_camera.start_video_stream(display=False)
    # sleep(3)
    result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
    # print(result)
    # try:

# def marker_program():
#     global result,count,x_data,y_data,x1,y1
    while result:
        try:
            img = ep_camera.read_cv2_image(strategy="newest")
            # print(img)
            # sleep(0.1)
            # print(img)
            cv2.imshow("Markers", img)
            cv2.waitKey(1)
            if y>yy:
            # if x>0.49 and x<0.51:
                ep_chassis.move(x=0, y=0, z=0, xy_speed=xy_spd).wait_for_completed()
                sleep(1)
                # print("stop")
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

                if y>0.535 and info=="1":
                    print("info:", info + " turn left")
                    count=count+1
                    # count=0
                    # print("turn left")
                    # ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_spd).wait_for_completed()
                    break
                elif y>yy and info=="2":
                    print("info:", info + " turn left")
                    count = count + 1
                    # print("info:", info)
                    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_spd).wait_for_completed()
                elif y>yy and info=="3":
                    print("info:", info + " turn left")
                    count = count + 1
                    # print("info:",info)
                    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_spd).wait_for_completed()
                elif y>yy and info == "4":
                    print("info:", info + " turn left")
                    count=count+1
                    # print("info:",info)
                    ep_chassis.move(x=0, y=0, z=-z_val, z_speed=z_spd).wait_for_completed()

            # if w>0.13 and info=="4":
            #     break
            else:
                if x < 0.475 and y>0.535:
                    print("moving left")
                    print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
                    ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=xy_spd).wait_for_completed()
                    if count ==0:
                        x_data=x_data-y_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==1:
                        y_data=y_data+y_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==2:
                        x_data=x_data+y_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==3:
                        y_data=y_data-y_val
                        x1.append(x_data)
                        y1.append(y_data)
                    # m=m+1

                if x > 0.525 and y>0.535:
                    print("moving right")
                    print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
                    ep_chassis.move(x=0, y=y_val, z=0, xy_speed=xy_spd).wait_for_completed()
                    if count ==0:
                        x_data=x_data+y_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==1:
                        y_data=y_data-y_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==2:
                        x_data=x_data-y_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==3:
                        y_data=y_data+y_val
                        x1.append(x_data)
                        y1.append(y_data)
                    # m+=1

                else:
                    ep_chassis.move(x=x_val, y=0, z=0, xy_speed=xy_spd).wait_for_completed()
                    if count ==0:
                        y_data=y_data+x_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==1:
                        x_data=x_data+x_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==2:
                        y_data=y_data-x_val
                        x1.append(x_data)
                        y1.append(y_data)
                    elif count ==3:
                        x_data=x_data-x_val
                        x1.append(x_data)
                        y1.append(y_data)
                    # m+=1

                    # if m==0:
                    #     x1.append(x_data)
                    #     y1.append(y_data)
                    # else:
                    #     pass

                    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
                    plt.show(block=False)
                    # sleep(1)
                    # m=m+1
                    # sleep(1)
                    # plt.close()

                    # y_data+=0.3
                    # x_data=0
                    # print("verts",verts)
                    print("move forward")
                    # print("count:",count)
                    # print(x1)
                    # print(y1)
                    # print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))

                    # verts.append(value)
        except:
            print("no markers detected")
            # print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
            pass


    # print("x1",x1)
    # print("y1",y1)
    # plt.plot(x1,y1,label="data1")
# marker_program()
plt.show()


result = ep_vision.unsub_detect_info(name="marker")
cv2.destroyAllWindows()
ep_camera.stop_video_stream()
ep_robot.close()