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
        self.canvas.delete('temp_objects')
        self.mouse_clicked = False
        #draws rectangle with first and last position of the cursor after dragging
        if self.x_pos and self.y_pos:
            self.draw(self.drawing_tool, self.color, self.size_button.get(), [self.x1, self.y1, self.x_pos, self.y_pos])
        self.x_pos = None
        self.y_pos = None

        # draws straight line with first and last position of the cursor after dragging

        self.x2 = event.x
        self.y2 = event.y

    def draw(self, tool, color, w, coordinates = []):
        if tool == "rectangle":
            x = self.canvas.create_rectangle(coordinates[0], coordinates[1], coordinates[2], coordinates[3], outline=color,
                                     width=w)
            self.Rectangles.append(x)
        # draws oval with first and last position of the cursor after dragging
        if tool == "oval":
            x = self.canvas.create_oval(coordinates[0], coordinates[1], coordinates[2], coordinates[3], outline=color,
                                width=w)
            self.Circles.append(x)
        if tool == "line":
            x = self.canvas.create_line(coordinates[0], coordinates[1], coordinates[2], coordinates[3], smooth=True, fill=color,
                                 width=w)
            self.Lines.append(x)
    
        self.stack.append([x, self.drawing_tool, color, w, [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]])

    def undo(self):
        properties = self.stack.pop()
        self.recentlyDeleted.append(properties)
        print(properties)
        self.canvas.delete(properties[0])

    def redo(self):
        recent = self.recentlyDeleted.pop()
        self.draw(recent[1],recent[2],recent[3],recent[4])
        self.canvas.insert(self.recentlyDeleted.pop())


    def motion(self, event=None):
        self.canvas.delete('temp_objects')
        if self.mouse_clicked:
            if self.x_pos is not None and self.y_pos is not None:
                if self.drawing_tool == "pencil":
                    x = self.canvas.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth=True, fill=self.color, width=self.size_button.get())
                    self.Drawing.append(x)
               #this eraser is simply a very thick pencil that has the same color with the background. I believe a better version may be implemented. Although this is a backup :)
                #elif self.drawing_tool == "eraser":
                    #event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth=True, fill="white", width=self.size_button.get()*5)
                elif self.drawing_tool == "rectangle":
                    self.canvas.create_rectangle(self.x1, self.y1, self.x_pos, self.y_pos, outline=self.color, width=self.size_button.get(),tags='temp_objects')          
                elif self.drawing_tool == "oval":
                    self.canvas.create_oval(self.x1, self.y1, self.x_pos, self.y_pos, outline=self.color, width=self.size_button.get(),tags="temp_objects")
                elif self.drawing_tool == "line":
                    self.canvas.create_line(self.x1, self.y1, self.x_pos, self.y_pos, fill=self.color, width=self.size_button.get(),tags="temp_objects")

            self.x_pos = event.x
            self.y_pos = event.y

    #displays color selector
    def choose_color(self):
        self.color = askcolor(color=self.color)[1]

    #these methods sets the brush type
    def set_brush_type(self, type):
        self.drawing_tool = type

    #def eraser_mode(self):
    #    self.drawing_tool = "eraser"

    def __init__(self, root):
        self.x = 0
        self.y = 0

        drawing_area = Canvas(width=450, height=500, background="white")
        drawing_area.pack(fill="both")
        drawing_area.bind("<Motion>", self.motion)
        drawing_area.bind("<ButtonPress-1>", self.clicked)
        drawing_area.bind("<ButtonRelease-1>", self.unclicked)
        self.canvas = drawing_area
        self.color = None
                
        self.Lines = []
        self.Circles = []
        self.Rectangles = []
        self.Drawing = []
        self.stack = []
        self.recentlyDeleted = []

        rect_button = tkinter.Button(text="Rectangle", command=lambda: self.set_brush_type("rectangle"))
        rect_button.pack(side="left", padx=55, pady=10)
        pencil_button = tkinter.Button(text="Pencil", command=lambda: self.set_brush_type("pencil"))
        pencil_button.pack(side="left", padx=60, pady=10)
        circle_button = tkinter.Button(text="Circle", command=lambda: self.set_brush_type("oval"))
        circle_button.pack(side="left", padx=65, pady=10)
        line_button = tkinter.Button(text="Line", command=lambda: self.set_brush_type("line"))
        line_button.pack(side="left", padx=70, pady=10)
        color_button = tkinter.Button(text="Color", command=self.choose_color)
        color_button.pack(side="left", padx=75, pady=10)
        #eraser_button = tkinter.Button(text="Eraser", command=self.eraser_mode)
        #eraser_button.pack(side="left", padx=80, pady=10)
        undo_button = tkinter.Button(text="undo", command=self.undo)
        undo_button.pack(side="left",padx=85, pady=10)
        redo_button = tkinter.Button(text="redo", command=self.redo)
        redo_button.pack(side="left",padx=85, pady=10)
        self.size_button = Scale(label="Thickness", from_=1, to=10, orient=HORIZONTAL)
        self.size_button.pack(side="left", padx=85, pady=10)
