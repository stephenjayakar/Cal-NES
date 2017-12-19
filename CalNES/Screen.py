import pygame
import time

class Screen:
    width = None
    height = None
    scale = None
    surface = None
    
    def __init__(self, width=256, height=240, scale=3):
        self.width = width * scale
        self.height = height * scale
        self.scale = scale
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(0)

    def SetRGBA(self, x, y, c):
        self.surface.fill(c, rect=pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))
