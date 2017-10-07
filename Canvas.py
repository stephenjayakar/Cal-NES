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
