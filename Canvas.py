import tkinter as tk

class Canvas(tk.Canvas):
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.root = tk.Tk()
        super().__init__(width=self.width, height=self.height, bg="white")
        self.pack()

    def clear(self):
        self.delete("all")
        self.pack()

top = tk.Tk()
C = tk.Canvas(top, bg="blue", height=340, width=360)
C2 = tk.Canvas(top, bg="blue", height=578, width=883)
filename = "Sprites/SNES - Super Mario World - Objects & Blocks.gif"
filename2 = "Sprites/SNES - Super Mario World - Ground Tiles.gif"
img_file = tk.PhotoImage(file=filename)
img_file2 = tk.PhotoImage(file=filename2)
image = C.create_image(185, 175, image=img_file)
image2 = C2.create_image(445, 180, image=img_file2)
C.pack()
C2.pack()
top.mainloop()