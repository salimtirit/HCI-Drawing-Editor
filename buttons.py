import tkinter
from tkinter import *

class Buttons:
        
    def __init__(self, drawing_app):
        self.rect_button = tkinter.Button(text="Rectangle", command=lambda: drawing_app.set_brush_type("rectangle"))
        self.rect_button.pack(side="left", padx=40, pady=10)
        self.pencil_button = tkinter.Button(text="Pencil", command=lambda: drawing_app.set_brush_type("pencil"))
        self.pencil_button.pack(side="left", padx=40, pady=10)
        self.circle_button = tkinter.Button(text="Circle", command=lambda: drawing_app.set_brush_type("oval"))
        self.circle_button.pack(side="left", padx=40, pady=10)
        self.line_button = tkinter.Button(text="Line", command=lambda: drawing_app.set_brush_type("line"))
        self.line_button.pack(side="left", padx=40, pady=10)
        self.select_button = tkinter.Button(text="Select Shapes", command=lambda: drawing_app.set_brush_type("select"))
        self.select_button.pack(side="left", padx=40, pady=10)
        self.move_button = tkinter.Button(text="Move Shapes", command=lambda: drawing_app.set_brush_type("move"))
        self.move_button.pack(side="left", padx=40, pady=10)
        self.delete_button = tkinter.Button(text="Delete", command=drawing_app.delete)
        self.delete_button.pack(side="left", padx=40, pady=10)
        self.color_button = tkinter.Button(text="Color", command=drawing_app.choose_color)
        self.color_button.pack(side="left", padx=40, pady=10)
        self.eraser_button = tkinter.Button(text="Eraser", command=drawing_app.eraser_mode)
        self.eraser_button.pack(side="left", padx=40, pady=10)
        self.undo_button = tkinter.Button(text="Undo", command=drawing_app.undo)
        self.undo_button.pack(side="left",padx=40, pady=10)
        self.redo_button = tkinter.Button(text="Redo", command=drawing_app.redo)
        self.redo_button.pack(side="left",padx=40, pady=10)
        self.size_button = Scale(label="Thickness", from_=1, to=10, orient=HORIZONTAL)
        self.size_button.pack(side="left", padx=40, pady=10)