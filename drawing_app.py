from tkinter import *
import tkinter.font

class DrawingApp:
    drawing_tool = "pencil"

    mouse_clicked = False

    x_pos, y_pos = None, None

    x1, y1, x2, y2 = None, None, None, None

    def clicked(self, event=None):
        self.mouse_clicked = True

        self.x1 = event.x
        self.y1 = event.y

    def unclicked(self, event=None):
        self.mouse_clicked = False

        self.x_pos = None
        self.y_pos = None

        self.x2 = event.x
        self.y2 = event.y

        if self.drawing_tool == "line":
            self.line_draw(event)

    def motion(self, event=None):
        if self.drawing_tool == "pencil" and self.mouse_clicked:
            if self.x_pos is not None and self.y_pos is not None: 
                event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth= True)
                
            self.x_pos = event.x
            self.y_pos = event.y

    def line_draw(self, event=None):
        if None not in (self.x1,self.y1,self.x2,self.y2):
            event.widget.create_line(self.x1, self.y1,self.x2,self.y2, smooth=True, fill="green")

    def __init__(self, root):
        drawing_area = Canvas()
        drawing_area.pack()
        drawing_area.bind("<Motion>", self.motion)
        drawing_area.bind("<ButtonPress-1>", self.clicked)
        drawing_area.bind("<ButtonRelease-1>", self.unclicked)

root = Tk()

drawing_app = DrawingApp(root)
root.mainloop()



