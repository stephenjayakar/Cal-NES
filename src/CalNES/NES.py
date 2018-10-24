from .ROM import ROM
from .RAM import ppuMEM
from .CPU import CPU
from .PPU import PPU
from .Joy import Joy, Button
from .Mapper import create_mapper
import pygame
import time
import os

class NES:
    __slots__ = ['rom', 'cpu', 'ppu', 'apu', 'mmap', 'surface', 'ram', 'vram', 'joy1']

    # TOOD: attach vram and ram to this, and point all references from ppu.mem
    def __init__(self, rom_name, DEBUG=False):
        self.rom = ROM(rom_name)
        self.ram = bytearray(0x10000)
        self.vram = ppuMEM(self)
        self.mmap = create_mapper(self, self.rom.mapper)
        self.mmap.reset()
        self.cpu = CPU(self, DEBUG)
        self.cpu.reset()
        self.ppu = PPU(self)
        self.surface = pygame.display.set_mode([256 * 3, 240 * 3])
        self.joy1 = Joy()

    def step(self):
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.QUIT:
                quit()            
        self.cpu.step()
        for i in range(3):
            self.ppu.step()
            self.mmap.step()
        # for i in range(cpu_cycles):
            # step the apu

    def current_buffer(self):
        return self.ppu.front

    def update_display(self):
        surface_buffer = self.current_buffer()
        self.surface.blit(surface_buffer.surface, (0, 0))
        pygame.display.update()

    def button_down(self, controller, button):
        if controller == 1:
            self.joy1.button_down(button)
        else:
            print("Controller {} is not supported yet".format(controller))

    def button_up(self, controller, button):
        if controller == 1:
            self.joy1.button_up(button)
        else:
            print("Controller {} is not supported yet".format(controller))
