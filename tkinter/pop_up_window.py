import tkinter as tk
from tkinter.messagebox import showinfo

# --- functions ---

def popup_window():
    window = tk.Toplevel()

    label = tk.Label(window, text="Hello World!")
    label.pack(fill='x', padx=50, pady=5)

    button_close = tk.Button(window, text="Close", command=window.destroy)
    button_close.pack(fill='x')

def popup_showinfo():
    showinfo("ShowInfo", "warning! The person is lying down!")

# --- main ---

root = tk.Tk()

button_bonus = tk.Button(root, text="Window", command=popup_window)
button_bonus.pack(fill='both')

button_showinfo = tk.Button(root, text="ShowInfo")
button_showinfo.pack(fill='x')

showinfo("ShowInfo", "warning! The person is lying down!")

button_close = tk.Button(root, text="Close", command=root.destroy)
button_close.pack(fill='x')

root.mainloop()