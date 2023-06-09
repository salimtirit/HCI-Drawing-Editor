from tkinter import *
from tkinter.colorchooser import askcolor
from buttons import Buttons

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

        if self.drawing_tool == "select": #select 
            self.select(event)
        elif self.drawing_tool != "move" and self.selected is not None: #unselect
            if self.selected in self.Lines:
                self.canvas.itemconfig(self.selected, fill="black")
            else:
                self.canvas.itemconfig(self.selected, outline="black")
            self.selected = None

        self.x1 = event.x
        self.y1 = event.y

    # when the user releases left mouse button
    def unclicked(self, event=None):
        self.canvas.delete('temp_objects')
        self.mouse_clicked = False
        #draws object with first and last position of the cursor after dragging
        if self.x_pos and self.y_pos or self.drawing_tool == "move":
            self.draw(self.drawing_tool, self.color, self.button.size_button.get(), [self.x1, self.y1, self.x_pos, self.y_pos])
        self.x_pos = None
        self.y_pos = None

        self.x2 = event.x
        self.y2 = event.y

    #draws the approprate shape on the canvas.  
    def draw(self, tool, color, w, coordinates = [], is_undo = False):
        if tool == "move" and self.selected is not None:
            #([x, self.drawing_tool, color, w, [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]])
            a = self.moving_object
            self.draw(a[1], a[2], a[3], self.last_coords)
            self.selected = None
            self.last_coords = None
            self.moving_object = None
            return
        else:
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

        # if is_undo:
        #     try:
        #         self.recentlyDeleted_operation.append("create")
        #         self.recentlyDeleted.append([x, tool, color, w, [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]])
        #     except:
        #         print("problem")
        # else:
        #     self.stack_operation.append("create")
        #     self.stack.append([x, self.drawing_tool, color, w, [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]])

    #undo s the last operation
    def undo(self):
        properties = self.stack.pop()
        self.recentlyDeleted.append(properties)
        self.canvas.delete(properties[0])
        # operation = self.stack_operation.pop()
        # if operation == "create":
        #     self.recentlyDeleted.append(properties)
        #     self.recentlyDeleted_operation.append("delete")
        #     self.canvas.delete(properties[0])
        # elif operation == "delete":
        #     self.draw(properties[1], properties[2], properties[3], properties[4], True)

    #redos the last undo operation
    def redo(self):
        recent = self.recentlyDeleted.pop()
        self.draw(recent[1],recent[2],recent[3],recent[4])
        # operation = self.recentlyDeleted_operation.pop()
        # if operation == "create":
        #     self.stack.append(recent)
        #     self.stack_operation.append("delete")
        #     self.canvas.delete(recent[0])
        # elif operation == "delete":    
        #     self.draw(recent[1], recent[2], recent[3], recent[4])
        
    #selects the closest object to the cursor and unselects the one that has been selected before.
    def select(self, event = None):
        if self.selected is not None:
            self.canvas.itemconfig(self.selected, outline="black")

        closest = self.canvas.find_closest(event.x, event.y)[0]

        if closest in self.Lines:
            self.canvas.itemconfig(closest, fill="red")
        else:
            self.canvas.itemconfig(closest, outline="red")

        for x in self.stack:
            if x[0] == closest:
              self.moving_object = x

        self.selected = closest

    #deletes the selected object
    def delete(self):
        if self.selected is not None:
            for object in self.stack:
                if object[0] == self.selected:
                    # self.stack.remove(object)
                    # self.stack.append(object)
                    # self.stack_operation.append("delete")
                    self.canvas.delete(self.selected)

    def motion(self, event=None):
        self.canvas.delete('temp_objects') # deletes the temporary objects. If the temp objects are not deleted all objects created along the way stays on the canvas.
        if self.mouse_clicked:
            if self.x_pos is not None and self.y_pos is not None:
                #create a smooth looking drawing using small lines.
                if self.drawing_tool == "pencil":
                    x = self.canvas.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth=True, fill=self.color, width=self.button.size_button.get())
                    self.Drawing.append(x)
                #this eraser is simply a very thick pencil that has the same color with the background. I believe a better version may be implemented. Although this is a backup :)
                elif self.drawing_tool == "eraser":
                    self.canvas.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth=True, fill="white", width=self.button.size_button.get()*5)
                #creates temporary rectangles while the user is moving the cursor with tag temp_objects.
                elif self.drawing_tool == "rectangle":
                    self.canvas.create_rectangle(self.x1, self.y1, self.x_pos, self.y_pos, outline=self.color, width=self.button.size_button.get(),tags='temp_objects')          
                #creates temporary ovals while the user is moving the cursor with tag temp_objects.
                elif self.drawing_tool == "oval":
                    self.canvas.create_oval(self.x1, self.y1, self.x_pos, self.y_pos, outline=self.color, width=self.button.size_button.get(),tags="temp_objects")
                #creates temporary lines while the user is moving the cursor with tag temp_objects.
                elif self.drawing_tool == "line":
                    self.canvas.create_line(self.x1, self.y1, self.x_pos, self.y_pos, fill=self.color, width=self.button.size_button.get(),tags="temp_objects")
                #creates temporary lines while the user is moving the cursor with tag temp_objects.
                elif self.drawing_tool == "move":
                    if self.moving_object in self.stack:
                        self.stack.remove(self.moving_object)
                        self.canvas.delete(self.moving_object[0])
                    coords_moving = self.moving_object[4]            
                    x_diff = coords_moving[0] - coords_moving[2]
                    y_diff = coords_moving[1] - coords_moving[3]
                    x_1 = event.x - x_diff/2
                    x_2 = event.x + x_diff/2
                    y_1 = event.y - y_diff/2
                    y_2 = event.y + y_diff/2
                    self.last_coords = [x_1, y_1, x_2, y_2]
                    #([x, self.drawing_tool, color, w, [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]])
                    if self.moving_object[1] == "rectangle":
                        self.canvas.create_rectangle(x_1, y_1, x_2, y_2, outline=self.moving_object[2], width=self.moving_object[3],tags='temp_objects')          
                    #creates temporary ovals while the user is moving the cursor with tag temp_objects.
                    elif self.moving_object[1] == "oval":
                        self.canvas.create_oval(x_1, y_1, x_2, y_2, outline=self.moving_object[2], width=self.moving_object[3],tags="temp_objects")
                    #creates temporary lines while the user is moving the cursor with tag temp_objects.
                    elif self.moving_object[1] == "line":
                        self.canvas.create_line(x_1, y_1, x_2, y_2, fill=self.moving_object[2], width=self.moving_object[3],tags="temp_objects")

                    self.canvas.coords(self.selected, coords_moving)
            self.x_pos = event.x
            self.y_pos = event.y

    #displays color selector
    def choose_color(self):
        self.color = askcolor(color=self.color)[1]

    #this method sets the brush type pencil, eraser, rectangle, oval, line or move
    def set_brush_type(self, type):
        self.drawing_tool = type

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
        self.selected = None        
        self.moving_object = None
        self.last_coords = None
        self.Lines = []
        self.Circles = []
        self.Rectangles = []
        self.Drawing = []
        self.stack = []
        self.stack_operation = []
        self.recentlyDeleted = []
        self.recentlyDeleted_operation = []

        self.button = Buttons(self)