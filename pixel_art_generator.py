from tkinter import *
import tkinter.colorchooser
from PIL import ImageGrab
from datetime import datetime


class PixelApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art")

        cell_length = 50
        grid_width = 20
        grid_height = 10

        self.colour_chooser = tkinter.colorchooser.Chooser(self.root)
        self.chosen_colour = None
        self.is_pen_selected = False
        self.is_eraser_selected = False


        self.drawing_grid = Canvas(self.root)
        self.drawing_grid.grid(column=0, row=0, sticky=(N, E, S, W))

        self.cells = []

        for row_num in range(grid_height):

            for column_num in range (grid_width):
                cell = Frame(self.drawing_grid, width=cell_length, height=cell_length, bg="white", highlightbackground="black", highlightcolor="black", highlightthickness=1)
                cell.grid(column=column_num, row=row_num)
                cell.bind("<Button-1>", self.tap_cell)
                self.cells.append(cell)

        control_frame = Frame(self.root, height=cell_length)
        control_frame.grid(column=0, row=1, sticky=(N, S, E, W))

        new_button = Button(control_frame, text="New", command=self.press_new_button)
        new_button.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W), padx=5 , pady=5)

        save_button = Button(control_frame, text="Save", command=self.press_save_button)
        save_button.grid(column=2, row=0, columnspan=2, sticky=(N, S, E, W), padx=5 , pady=5)

        self.pen_image = PhotoImage(file="icons/pencil.png").subsample(2,3)
        pen_button = Button(control_frame, text="pen", image=self.pen_image, command=self.press_pen_button)
        pen_button.grid(column=8, row=0, columnspan=2, sticky=(N, S, E, W), padx=5 , pady=5)

        self.eraser_image = PhotoImage(file="icons/eraser.png").subsample(2,3)
        erase_button = Button(control_frame, text="Erase", image=self.eraser_image, command=self.press_erase_button)
        erase_button.grid(column=10, row=0, columnspan=2, sticky=(N, S, E, W), padx=5 , pady=5)

        self.selected_colour_box = Frame(control_frame, borderwidth=2, relief="raised", bg="white")
        self.selected_colour_box.grid(column=15, row=0, sticky=(N, E, S, W), padx=5 , pady=8)

        pick_colour_button = Button(control_frame, text="Pick Colour", command=self.press_pick_colour_button)
        pick_colour_button.grid(column=17, row=0, columnspan=3, sticky=(N, S, E, W), padx=5 , pady=5) 

        cols, rows = control_frame.grid_size()
        for col in range(cols):
            control_frame.columnconfigure(col, minsize=cell_length)
        control_frame.rowconfigure(0, minsize=cell_length)

        
    def tap_cell(self, event):
        widget = event.widget
        index = self.cells.index(widget)
        selected_cell = self.cells[index]

        if self.is_eraser_selected:
            selected_cell["bg"] = "white"

        if self.is_pen_selected and self.chosen_colour != None:
            selected_cell["bg"] = self.chosen_colour 

    def press_new_button(self):
        for cell in self.cells:
            cell["bg"] = "white"
        self.selected_colour_box["bg"] = "white"
        self.chosen_colour = None
        self.is_pen_selected = False
        self.is_eraser_selected = False


    def press_save_button(self):
        
        x = self.root.winfo_rootx() + self.drawing_grid.winfo_x() - 15  
        y = self.root.winfo_rooty() + self.drawing_grid.winfo_y() + 15

        width = x + 1250        
        height = y + 625

        image_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".png"
        _ = ImageGrab.grab(bbox=(x, y, width, height)).save(image_name)
                
    def press_pen_button(self):

        self.is_pen_selected = True
        self.is_eraser_selected = False
        
    def press_erase_button(self):

        self.is_pen_selected = False
        self.is_eraser_selected = True

    def press_pick_colour_button(self):

        colour_info = self.colour_chooser.show()
        chosen = colour_info[1]

        if chosen != None:
            self.chosen_colour = chosen 
            self.selected_colour_box["bg"] = self.chosen_colour

root =Tk()
PixelApp(root)
root.mainloop()