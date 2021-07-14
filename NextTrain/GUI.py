from tkinter import *
from PIL import Image, ImageTk

# #region Dragging code
def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

class DragDropMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        make_draggable(self)

class DnDFrame(DragDropMixin, Frame):
    pass
# #endregion

class Widgets:
    def __init__(self, image, size):
        dnd = Button(map, image = station_img, bg = "white", relief = FLAT)
        make_draggable(dnd)
        dnd.place(x=20,y=20)

stations = []

def create_widget(event):
    stations.append(Widgets("station", 4))

# create window
window = Tk()
window.title("NextTrain")

photo = PhotoImage(file = r"D:\Users\Vaughan Bunt\Documents\School\year 3\advanced studio2\NextTrain\station.png")
photoimage = photo.subsample(4, 4)
station_img = photoimage

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(0, minsize=800, weight=1)

map = Frame(window, width=100, height=100, bg="white")
fr_buttons = Frame(window, bg="grey")
btn_station = Button(fr_buttons, image=station_img, relief = FLAT, bg="grey")
btn_junction = Button(fr_buttons, text="Create Junction")

btn_station.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_junction.grid(row=1, column=0, sticky="ew", padx=5)

map.grid(row=0, column=0, sticky="nsew")
fr_buttons.grid(row=0, column=1, sticky="ns")

btn_station.bind("<Button-1>", create_widget)

window.mainloop()
