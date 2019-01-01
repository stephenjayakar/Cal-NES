#!/usr/bin/env python3

from CalNES.NES import NES
from CalNES.Joy import Button
import sys
import time
import pygame

controls = {
    pygame.K_a: Button.LEFT,
    pygame.K_s: Button.DOWN,
    pygame.K_d: Button.RIGHT,
    pygame.K_w: Button.UP,
    pygame.K_j: Button.A,
    pygame.K_k: Button.B,
    pygame.K_q: Button.SELECT,
    pygame.K_e: Button.START
}

def debug_vram():
    FILE = open('temp.dat', 'wb')
    for i in range(0x3fff):
        FILE.write(bytearray([n.vram[i]]))
    FILE.close()

filename = sys.argv[1]
DEBUG = True if (len(sys.argv) > 2 and sys.argv[2] == '-d') else False
n = NES(filename, DEBUG)
timer = time.time()
while True:
    for event in pygame.event.get():
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = event.key
            if key in controls:
                button = controls[key]
                if event.type == pygame.KEYDOWN:
                    n.button_down(1, button)
                else:
                    n.button_up(1, button)
        elif event.type == pygame.QUIT:
            quit()
    n.step()
    cur_time = time.time()
    if cur_time - timer >= 0.16639:
        timer = cur_time
        n.update_display()
