import tkinter as tk


palette = ["white", "red", "green", "blue"]


class Display(tk.Canvas):
    width = 0
    height = 0
    
    def __init__(self, width=256, height=240, scale=4):
        self.width = width * scale
        self.height = height * scale
        self.scale = scale
        self.root = tk.Tk()
        super().__init__(width=self.width, height=self.height, bg="black")
        self.pack()

    def draw_tile(self, lst: list, x_offset: int, y_offset: int):
        scale = self.scale
        x_offset = x_offset * scale * 8 + 10
        y_offset = y_offset * scale * 8 + 10
        x = 0
        y = 0
        for choice in lst:
            y = x // 8
            xcoord = ((x % 8) * scale) + x_offset
            ycoord = y * scale + y_offset
            self.create_rectangle(xcoord, ycoord, xcoord + scale, ycoord + scale, fill=palette[choice])
            x += 1
        self.pack()
    
