import pygame
import time

class Display:
    width = None
    height = None
    scale = None
    screen = None
    
    def __init__(self, width=256, height=240, scale=4):
        self.width = width * scale
        self.height = height * scale
        self.scale = scale
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(0)
        pygame.display.update()

    def SetRGBA(self, x, y, c):
        print(c)

    def update(self):
        pygame.display.update()

    # def draw_tile(self, lst: list, x_offset: int, y_offset: int):
    #     scale = self.scale
    #     x_offset = x_offset * scale * 8 + 10
    #     y_offset = y_offset * scale * 8 + 10
    #     x = 0
    #     y = 0
    #     for choice in lst:
    #         y = x // 8
    #         xcoord = ((x % 8) * scale) + x_offset
    #         ycoord = y * scale + y_offset
    #         # self.create_rectangle(xcoord, ycoord, xcoord + scale, ycoord + scale, fill=palette[choice])
    #         self.screen.fill(palette[choice], rect=pygame.Rect(xcoord, ycoord, scale, scale))
    #         x += 1
        
if __name__ == "__main__":
    d = Display()
    while True:
        print(pygame.event.get())

# import tkinter as tk


# palette = ["white", "green", "blue", "red"]


# class Display(tk.Canvas):
#     width = 0
#     height = 0
    
#     def __init__(self, width=256, height=240, scale=4):
#         self.width = width * scale
#         self.height = height * scale
#         self.scale = scale
#         self.root = tk.Tk()
#         super().__init__(width=self.width, height=self.height, bg="black")
#         self.pack()

#     def draw_tile(self, lst: list, x_offset: int, y_offset: int):
#         scale = self.scale
#         x_offset = x_offset * scale * 8 + 10
#         y_offset = y_offset * scale * 8 + 10
#         x = 0
#         y = 0
#         for choice in lst:
#             y = x // 8
#             xcoord = ((x % 8) * scale) + x_offset
#             ycoord = y * scale + y_offset
#             self.create_rectangle(xcoord, ycoord, xcoord + scale, ycoord + scale, fill=palette[choice])
#             x += 1
#         self.pack()
    
