# from tkinter import *
# from PIL import ImageTk,Image
# root = Tk()
# canvas = Button(root, width = 300, height = 300)
# canvas.pack()
# img = ImageTk.PhotoImage(Image.open("frog.png"))
# canvas.create_image(20, 20, anchor=NW, image=img)
# root.mainloop()

from tkinter import *
root=Tk()

photo=PhotoImage(file="frog.png")
# photo1=PhotoImage(file=r"D:\downloads\arrow.png")

button=Button(root, image=photo,height=100,width=100).grid(row=0,column=0)

mainloop()
