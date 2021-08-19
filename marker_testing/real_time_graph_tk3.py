import tkinter as tk
from PIL import ImageTk, Image
import cv2
import robomaster
from robomaster import robot
from robomaster import vision
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading

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


# ani=0
m=0
count=0
x_data=0
y_data=0
x1=[]
y1=[]
toggle=0

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

# continuePlotting = False
#
# def change_state():
#     global continuePlotting
#     if continuePlotting == True:
#         continuePlotting = False
#     else:
#         continuePlotting = True

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis

    ep_camera.start_video_stream(display=False)
    # sleep(3)
    result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)

def video_stream():
    img = ep_camera.read_cv2_image(strategy="newest")
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image, "RGB")
    # print(img)
    imgtk = ImageTk.PhotoImage(image=img)
    # print(imgtk)
    main_label.imgtk = imgtk
    main_label.configure(image=imgtk)
    main_label.after(1, video_stream)

def stop_video_stream():
    global result
    window.destroy()
    result = ep_vision.unsub_detect_info(name="marker")
    ep_camera.stop_video_stream()
    ep_robot.close()

def plotter():
    # while result:
    ax.cla()
    ax.grid()
    ax.plot(x1,y1,marker="o",color="blue",)
    graph.draw()
    time.sleep(1)

def marker_program():
    # result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
    global count,x_data,y_data,x1,y1
    while toggle>0:
        # print("hi")
        # result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
        try:

            if y>yy:
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

                if y>0.535 and info=="1":
                    # print("info:", info + " turn left")
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

                print("1")
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
                    print("move forward")
                    print("2")
                    plotter()

        except:
            print("no markers detected")
            pass

window=tk.Tk()
window.geometry("1920x1280")

app=tk.Frame(window,bg="white")
app.place(relwidth=1,relheight=1)

main_label=tk.Label(app,bg="black")
main_label.place(relheight=0.7,relwidth=0.5)

lab=tk.Label(app)
lab.place(relx=0.5,relheight=0.7,relwidth=0.5)

fig = Figure()

ax = fig.add_subplot(111)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.grid()

graph = FigureCanvasTkAgg(fig, master=lab)
graph.get_tk_widget().pack(side="top", fill='both', expand=True)

button=tk.Button(app,text="stop",command=stop_video_stream)
button.place(rely=0.7,relheight=0.1,relwidth=0.5)
# button.bind("<Button-1>",button_press)

# button1=tk.Button(app,text="on vs")
button1=tk.Button(app,text="on vs",command=video_stream)
button1.place(rely=0.7,relx=0.5,relheight=0.1,relwidth=0.5)

button2=tk.Button(app,text="marker program",command=marker_program)
# button2=tk.Button(app,text="marker program")
button2.place(rely=0.8,relheight=0.1,relwidth=0.5)

# def gui_handler():
#     change_state()
#     threading.Thread(target=plotter).start()

def toggle_prog():
    global toggle
    toggle +=1
    print("toggle:",toggle)
    if toggle ==2:
        print("reset toggle")
        toggle = 0

b = tk.Button(app, text="Start/Stop", command=toggle_prog)
b.place(rely=0.8,relx=0.5,relheight=0.1,relwidth=0.5)

window.mainloop()