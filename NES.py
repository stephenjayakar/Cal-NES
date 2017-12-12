from ROM import ROM
from RAM import RAM
from CPU import CPU
from PPU import PPU
import pygame
import time
import os

class NES:
    rom = None
    ram = None
    ppu_ram = None
    cpu = None
    ppu = None
    apu = None
    
    def __init__(self, rom_name: str):
        self.rom = ROM(rom_name)
        self.ram = RAM()
        self.ppu_ram = RAM()
        self.cpu = CPU(self.ram)
        self.ppu = PPU(self, self.ppu_ram)
        
        # Instructions start at 0x8000 / prg_rom
        # self.ram.mem_set(0x8000, bytearray(self.rom.prg_rom))
        self.ram.mem_set(0x8000, bytearray(self.rom.prg_rom[0x37:]))

        # Should start at 0
        self.ppu_ram.mem_set(0, bytearray(self.rom.chr_rom))
        
        
        
if __name__ == "__main__":
    offset = 0
    n = NES("smb.nes")
    start_time = time.time()
    while True:
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.QUIT:
                quit()
        # n.cpu.tick()
        n.ppu.tick()
        if time.time() - start_time >= .016639:
            start_time = time.time()
            n.ppu.update_display()
    print("Done")
