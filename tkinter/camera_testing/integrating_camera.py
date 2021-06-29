import tkinter as tk
from PIL import ImageTk, Image
import cv2
from robomaster import robot
import os

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_camera = ep_robot.camera

# capture= cv2.VideoCapture(0)
capture = ep_camera.start_video_stream(display=False)

def video_stream():
    # global capture

    # print(capture)
    #
    # _, frame = capture.read()

    # print(frame)

    # print(capture.read())

    # cv2image = cv2.cvtColor(capture, cv2.COLOR_BGR2RGBA)

    # print("cv2image:",cv2image)
    # img = Image.fromarray(cv2image)

    img = ep_camera.read_cv2_image(strategy="newest")
    # cv2.imshow("Robot", img)
    # cv2.waitKey(1)

    # print(type(capture))

    cv2image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # img = Image.fromarray(cv2image)

    # cv2image = cv2.cvtColor(img.astype('float32'), cv2.COLOR_BGR2RGB)
    img=Image.fromarray(cv2image,"RGB")

    imgtk=ImageTk.PhotoImage(image=img)
    # print(img)
    main_label.imgtk=imgtk
    main_label.configure(image=imgtk)
    main_label.after(1,video_stream)

count=0

def screenshot(capture,path_output_dir):
    global count
    print("screenshot")
    print(count)
    # count=count
    # while capture.isOpened():
    while count<10:
        img2=ep_camera.read_cv2_image()
        cv2.imwrite(os.path.join(path_output_dir,'%d.png')%count,img2)
        count=count+1
        break

def button_press(event):
    screenshot(capture,r"C:\Users\Mikehang\OneDrive\Pictures\Saved Pictures\reee")
    print("clicked")

window=tk.Tk()
window.geometry("1300x750")

app=tk.Frame(window,bg="white")
app.place(relwidth=1,relheight=1)

main_label=tk.Label(app)
main_label.place(relheight=0.5,relwidth=0.5)

button=tk.Button(app,text="snapshot")
button.place(rely=0.5,relheight=0.1,relwidth=0.5)
button.bind("<Button-1>",button_press)

button1=tk.Button(app,text="on vs",command=video_stream)
button1.place(rely=0.6,relheight=0.1,relwidth=0.5)

# print("capture:",capture)

# video_stream()
window.mainloop()
