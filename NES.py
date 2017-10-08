from ROM import ROM
from RAM import RAM
from CPU import CPU
from PPU import PPU
import time

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
        self.ram.mem_set(0x8000, bytearray(self.rom.prg_rom))

        # Should start at 0
        self.ppu_ram.mem_set(0, bytearray(self.rom.chr_rom))
        
        
def test():
    global offset
    print(offset)
    n.ppu.display.after(500, test)
    n.ppu.draw_pattern(offset)
    offset += 16
        
if __name__ == "__main__":
    offset = 0
    n = NES("smb.nes")
    n.ppu.display.after(500, test)
    n.ppu.display.mainloop()
    while True:
        pass
    print("Done")
