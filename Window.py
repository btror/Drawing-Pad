import tkinter as tk
from tkinter import *
from tkinter import colorchooser
from tkinter import simpledialog
from PIL import Image, ImageTk


class Window:
    def __init__(self):
        # default values
        self.color = "black"
        self.outline_color = "black"
        self.canvas_color = "white"
        self.draw_size = 1
        self.draw_shape = "oval"
        self.eraser_enabled = False
        self.current_button = "draw"

        # setup window
        self.root = tk.Tk()
        self.root.geometry("900x700")
        self.root.title("Drawing Pad")
        self.root.resizable(True, True)

        # setup menu
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)

        toolbar = Frame(self.root, bd=1, )

        pencil_holder = Label(toolbar)
        pencil_holder.pack(side=LEFT)
        img_pencil = Image.open("images/pencil_draw.png")
        img_pencil_resize = img_pencil.resize((40, 40), Image.ANTIALIAS)
        icon_pencil = ImageTk.PhotoImage(img_pencil_resize)
        self.draw_button = Button(pencil_holder, image=icon_pencil, relief=FLAT, command=self.draw)
        self.draw_button.pack(side=TOP, fill=X, padx=15, pady=5)
        self.paint_size = draw_size_spin = Spinbox(pencil_holder, from_=1, to=75, width=5)
        draw_size_spin.pack(pady=5)

        # get original background color
        self.original_button_color = self.draw_button.cget("background")

        pencil_eraser_holder = Label(toolbar)
        pencil_eraser_holder.pack(side=LEFT)
        img_pencil_eraser = Image.open("images/pencil_eraser.png")
        img_pencil_eraser_resize = img_pencil_eraser.resize((40, 40), Image.ANTIALIAS)
        icon_pencil_eraser = ImageTk.PhotoImage(img_pencil_eraser_resize)
        self.pencil_eraser_button = Button(pencil_eraser_holder, image=icon_pencil_eraser, relief=FLAT, command=self.erase)
        self.pencil_eraser_button.pack(side=TOP, padx=15, pady=5)
        self.erase_size = pencil_eraser_size = Spinbox(pencil_eraser_holder, from_=1, to=75, width=5)
        pencil_eraser_size.pack(pady=5)

        eraser_holder = Label(toolbar)
        eraser_holder.pack(side=LEFT)
        img_eraser = Image.open("images/eraser.png")
        img_eraser_resize = img_eraser.resize((40, 40), Image.ANTIALIAS)
        icon_eraser = ImageTk.PhotoImage(img_eraser_resize)
        self.eraser_button = Button(eraser_holder, image=icon_eraser, relief=FLAT, command=self.clear_canvas)
        self.eraser_button.pack(side=TOP, padx=15, pady=5)
        eraser_label = Label(eraser_holder, text="Clear all")
        eraser_label.pack(pady=5)

        bg_holder = Label(toolbar)
        bg_holder.pack(side=LEFT)
        img_bg_color = Image.open("images/rgb_pic.png")
        img_bg_color_resize = img_bg_color.resize((40, 40), Image.ANTIALIAS)
        icon_bg_color = ImageTk.PhotoImage(img_bg_color_resize)
        self.bg_color_button = Button(bg_holder, image=icon_bg_color, relief=FLAT, command=self.change_canvas_color)
        self.bg_color_button.pack(side=TOP, padx=15, pady=5)
        bg_label = Label(bg_holder, text="Background")
        bg_label.pack(pady=5)

        draw_holder = Label(toolbar)
        draw_holder.pack(side=LEFT)
        img_draw_color = Image.open("images/rgb_pic.png")
        img_draw_color_resize = img_draw_color.resize((40, 40), Image.ANTIALIAS)
        icon_draw_color = ImageTk.PhotoImage(img_draw_color_resize)
        self.draw_color_button = Button(draw_holder, image=icon_draw_color, relief=FLAT, command=self.change_draw_color)
        self.draw_color_button.pack(side=TOP, padx=15, pady=5)
        draw_label = Label(draw_holder, text="Drawing")
        draw_label.pack(pady=5)

        # save_holder = Label(toolbar)
        # save_holder.pack(side=LEFT)
        # img_save = Image.open("images/save_icon.png")
        # img_save_resize = img_save.resize((40, 40), Image.ANTIALIAS)
        # icon_save = ImageTk.PhotoImage(img_save_resize)
        # self.save_button = Button(save_holder, image=icon_save, relief=FLAT, command=self.do_nothing)
        # self.save_button.pack(side=TOP, padx=15, pady=5)
        # save_label = Label(save_holder, text="Save as")
        # save_label.pack(pady=5)

        toolbar.pack(side=TOP, fill=X)

        file_menu.add_command(label="clear canvas", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="draw color", command=self.change_draw_color)
        file_menu.add_command(label="  -fill color", command=self.change_draw_fill_color)
        file_menu.add_command(label="  -outline color", command=self.change_draw_outline_color)
        file_menu.add_command(label="canvas color", command=self.change_canvas_color)
        file_menu.add_separator()
        file_menu.add_command(label="draw size", command=self.change_draw_size)
        file_menu.add_command(label="draw squares", command=self.change_draw_shape_to_square)
        file_menu.add_command(label="draw circles", command=self.change_draw_shape_to_oval)

        menu_bar.add_cascade(label="Advanced", menu=file_menu)
        self.root.config(menu=menu_bar)

        # setup drawing canvas
        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, bg="white", width=window_width, height=window_height)
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)

        # show window
        self.root.mainloop()

    def paint(self, event):
        x1, y1 = (event.x - int(self.paint_size.get())), (event.y - int(self.paint_size.get()))
        x2, y2 = (event.x + int(self.paint_size.get())), (event.y + int(self.paint_size.get()))
        x1e, y1e = (event.x - int(self.erase_size.get())), (event.y - int(self.erase_size.get()))
        x2e, y2e = (event.x + int(self.erase_size.get())), (event.y + int(self.erase_size.get()))
        if not self.eraser_enabled:
            if self.draw_shape == "square":
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline=self.outline_color)
            else:
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.outline_color)
        else:
            self.canvas.create_rectangle(x1e, y1e, x2e, y2e, fill=self.canvas_color, outline=self.canvas_color)

    def change_draw_color(self):
        color_code = colorchooser.askcolor(title="select draw color")
        self.color = color_code[1]
        self.outline_color = color_code[1]
        self.highlight_button("draw_color")

    def change_draw_fill_color(self):
        color_code = colorchooser.askcolor(title="select fill color")
        self.color = color_code[1]

    def change_draw_outline_color(self):
        color_code = colorchooser.askcolor(title="select outline color")
        self.outline_color = color_code[1]

    def change_canvas_color(self):
        color_code = colorchooser.askcolor(title="select canvas color")
        self.canvas_color = color_code[1]
        self.canvas.configure(bg=self.canvas_color)
        self.highlight_button("canvas_color")

    def change_draw_size(self):
        self.draw_size = simpledialog.askinteger("Input", "Enter a size", parent=self.root)

    def change_draw_shape_to_oval(self):
        self.draw_shape = "oval"

    def change_draw_shape_to_square(self):
        self.draw_shape = "square"

    def clear_canvas(self):
        self.canvas.delete("all")
        self.highlight_button("clear_canvas")

    def erase(self):
        self.eraser_enabled = True
        self.highlight_button("erase")

    def draw(self):
        self.eraser_enabled = False
        self.highlight_button("draw")

    def highlight_button(self, button_name):
        self.current_button = button_name
        # draw_color
        # canvas_color
        # clear_canvas
        # erase
        # draw
        if button_name == "draw_color":
            self.draw_color_button.config(background="lightblue")
            # remove bg color from other buttons
            self.bg_color_button.config(background=self.original_button_color)
            self.eraser_button.config(background=self.original_button_color)
            self.pencil_eraser_button.config(background=self.original_button_color)
            self.draw_button.config(background=self.original_button_color)

        if button_name == "canvas_color":
            self.bg_color_button.config(background="lightblue")
            # remove bg color from other buttons
            self.draw_color_button.config(background=self.original_button_color)
            self.eraser_button.config(background=self.original_button_color)
            self.pencil_eraser_button.config(background=self.original_button_color)
            self.draw_button.config(background=self.original_button_color)

        if button_name == "clear_canvas":
            self.eraser_button.config(background="lightblue")
            # remove bg color from other buttons
            self.bg_color_button.config(background=self.original_button_color)
            self.draw_color_button.config(background=self.original_button_color)
            self.pencil_eraser_button.config(background=self.original_button_color)
            self.draw_button.config(background=self.original_button_color)

        if button_name == "erase":
            self.pencil_eraser_button.config(background="lightblue")
            # remove bg color from other buttons
            self.eraser_button.config(background=self.original_button_color)
            self.bg_color_button.config(background=self.original_button_color)
            self.draw_color_button.config(background=self.original_button_color)
            self.draw_button.config(background=self.original_button_color)

        if button_name == "draw":
            self.draw_button.config(background="lightblue")
            # remove bg color from other buttons
            self.pencil_eraser_button.config(background=self.original_button_color)
            self.eraser_button.config(background=self.original_button_color)
            self.bg_color_button.config(background=self.original_button_color)
            self.draw_color_button.config(background=self.original_button_color)


    def do_nothing(self):
        x = 10


window = Window()
