from .ROM import ROM
from .RAM import cpuMEM, ppuMEM
from .CPU import CPU
from .PPU import PPU
from .Mapper import create_mapper
import pygame
import time
import os

class NES:
    __slots__ = ['rom', 'ram', 'cpu', 'ppu', 'apu', 'mapper', 'surface']    
    def __init__(self, rom_name):
        self.rom = ROM(rom_name)
        self.mapper = create_mapper(self.rom)
        self.ram = bytearray(0x10000)
        self.cpu = CPU(cpuMEM(self))
        self.ppu = PPU(self, ppuMEM(self))
        self.surface = pygame.display.set_mode([256 * 3, 240 * 3])

    # TODO: how often do we call this?  This seems to have an arbitrary amount of cycles
    def step(self):
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.QUIT:
                quit()            
        self.cpu.step()
        for i in range(3):
            self.ppu.step()
            self.mapper.step()
        #for i in range(cpu_cycles):
            # step the apu
         #   pass 

    # why does this return an int
    # def step_frame(self):
    #     cpu_cycles = 0
    #     frame = self.ppu.frame
    #     while frame == self.ppu.frame:
    #         cpu_cycles += self.step()
    #     return cpu_cycles

    def current_buffer(self):
        return self.ppu.front

    def update_display(self):
        surface_buffer = self.current_buffer()
        self.surface.blit(surface_buffer.surface, (0, 0))
        pygame.display.update()

        
def main():
    offset = 0
    n = NES("mb.nes")
    display_start_time = time.time()
    clock_start_time = time.time()
    while True:
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.QUIT:
                quit()
        # if time.time() - clock_start_time >= .00000055873007359033799258341700316185:
            # clock_start_time = time.time()
        n.step()
        if time.time() - display_start_time >= .016639:
            display_start_time = time.time()
            n.update_display()
    print("Done")
    
if __name__ == "__main__":
    main()
