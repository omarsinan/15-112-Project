from Tkinter import *

# wButton template:
# btn_width, btn_height = 100, 50
# x = (WIDTH / 2) - (btn_width / 2)
# y = start_y + 280
# regBtn = widgets.wButton(parent=self.registerFrame, width=btn_width, height=btn_height, x=x, y=y, bg="orange",func=self.registerUser, text="Register")
class wButton():
    def __init__(self, parent=None, width=50, height=25, x=0, y=0, bg="black", func=None, *args, **kwargs):
        self.f = Frame(parent, height=height, width=width, bg=bg)
        self.f.pack_propagate(0)
        self.f.place(x=x-(width/2), y=y-(height/2))
        self.label = Label(self.f, bg=bg, *args, **kwargs)
        self.label.place(x=width/2, y=height/2, width=width, height=height, anchor="center")
        self.label.bind("<Button-1>", func)