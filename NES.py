from ROM import ROM
from RAM import RAM
from CPU import CPU
from PPU import PPU
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
        self.ppu = PPU(self.ram, self.ppu_ram)
        
        # Instructions start at 0x8000 / prg_rom
        # self.ram.mem_set(0x8000, bytearray(self.rom.prg_rom))
        self.ram.mem_set(0x8000, bytearray(self.rom.prg_rom[0x37:]))

        # Should start at 0
        self.ppu_ram.mem_set(0, bytearray(self.rom.chr_rom))
        
        
def test():
    global offset
    n.ppu.display.after(1000, test)
    os.system("cls")
    n.cpu.tick()
    print(n.cpu._cpu_dump())
    offset += 16
        
if __name__ == "__main__":
    offset = 0
    n = NES("zelda_test.nes")
    # n.ppu.display.after(1000, test)
    # n.ppu.display.mainloop()
    while True:
        n.cpu.tick()
        n.ppu.tick()
        print(n.cpu._cpu_dump())
    print("Done")
