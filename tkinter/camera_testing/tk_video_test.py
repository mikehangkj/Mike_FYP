import tkinter as tk
from PIL import ImageTk, Image
import cv2
from robomaster import robot

def video_stream():
    img = ep_camera.read_cv2_image()
    cv2image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img=Image.fromarray(cv2image,"RGB")
    imgtk=ImageTk.PhotoImage(image=img)
    main_label.imgtk=imgtk
    main_label.configure(image=imgtk)
    main_label.after(1,video_stream)

def stop_video_stream():
    ep_camera.stop_video_stream()
    ep_robot.close()
    window.destroy()

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_camera = ep_robot.camera

capture = ep_camera.start_video_stream(display=False)

window=tk.Tk()
window.geometry("1300x750")

app=tk.Frame(window,bg="white")
app.place(relwidth=1,relheight=1)

main_label=tk.Label(app)
main_label.place(relheight=0.5,relwidth=0.5)

button=tk.Button(app,text="stop",command=stop_video_stream)
button.place(rely=0.5,relheight=0.1,relwidth=0.5)

button_1=tk.Button(app,text="start",command=video_stream)
button_1.place(rely=0.6,relheight=0.1,relwidth=0.5)

video_stream()
window.mainloop()

