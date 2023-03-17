import tkinter
from tkinter import *
from tkinter.colorchooser import askcolor


class DrawingApp:
    #default color and brush values
    drawing_tool = "pencil"
    mouse_clicked = False
    color = "black"

    x_pos, y_pos = None, None  # current position of the mouse

    x1, y1, x2, y2 = None, None, None, None  # first and last position of the mouse when using line, rectangle etc

    # when the user clicks left mouse button
    def clicked(self, event=None):
        self.mouse_clicked = True

        self.x1 = event.x
        self.y1 = event.y

    # when the user releases left mouse button
    def unclicked(self, event=None):
        self.mouse_clicked = False
        #draws rectangle with first and last position of the cursor after dragging
        if self.x_pos and self.y_pos and self.drawing_tool == "rectangle":
            self.canvas.create_rectangle(self.x1, self.y1, self.x_pos, self.y_pos, outline=self.color,
                                         width=self.size_button.get())
        # draws oval with first and last position of the cursor after dragging
        if self.x_pos and self.y_pos and self.drawing_tool == "oval":
            self.canvas.create_oval(self.x1, self.y1, self.x_pos, self.y_pos, outline=self.color,
                                    width=self.size_button.get())
        # draws straight line with first and last position of the cursor after dragging
        if self.x_pos and self.y_pos and self.drawing_tool == "line":
            self.line_draw(event)

        self.x_pos = None
        self.y_pos = None

        self.x2 = event.x
        self.y2 = event.y



    def motion(self, event=None):
        if self.mouse_clicked:
            if self.x_pos is not None and self.y_pos is not None and self.drawing_tool == "pencil":
                event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth=True, fill=self.color,
                                         width=self.size_button.get())
            self.x_pos = event.x
            self.y_pos = event.y

    def line_draw(self, event=None):
        if None not in (self.x1, self.y1, self.x2, self.y2):
            event.widget.create_line(self.x1, self.y1, self.x2, self.y2, smooth=True, fill=self.color,
                                     width=self.size_button.get())
    #displays color selector
    def choose_color(self):
        self.color = askcolor(color=self.color)[1]

    #these methods sets the brush type
    def rect_mode(self):
        self.drawing_tool = "rectangle"

    def oval_mode(self):
        self.drawing_tool = "oval"

    def pencil_mode(self):
        self.drawing_tool = "pencil"

    def line_mode(self):
        self.drawing_tool = "line"

    def __init__(self, root):
        self.x = 0
        self.y = 0

        drawing_area = Canvas(width=400, height=450)
        drawing_area.pack(fill="both")
        drawing_area.bind("<Motion>", self.motion)
        drawing_area.bind("<ButtonPress-1>", self.clicked)
        drawing_area.bind("<ButtonRelease-1>", self.unclicked)
        self.canvas = drawing_area
        self.color = None

        rect_button = tkinter.Button(text="Rectangle", command=self.rect_mode)
        rect_button.pack(side="left", padx=55, pady=10)
        pencil_button = tkinter.Button(text="Pencil", command=self.pencil_mode)
        pencil_button.pack(side="left", padx=60, pady=10)
        circle_button = tkinter.Button(text="Circle", command=self.oval_mode)
        circle_button.pack(side="left", padx=65, pady=10)
        line_button = tkinter.Button(text="Line", command=self.line_mode)
        line_button.pack(side="left", padx=70, pady=10)
        color_button = tkinter.Button(text="Color", command=self.choose_color)
        color_button.pack(side="left", padx=75, pady=10)
        self.size_button = Scale(label="Thickness", from_=1, to=10, orient=HORIZONTAL)
        self.size_button.pack(side="left", padx=80, pady=10)
