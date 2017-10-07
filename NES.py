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

        # Not sure what the start offset is 
        self.ppu_ram.mem_set(0, bytearray(self.rom.chr_rom))
        
        # Only runs one instruction
        self.cpu.run_instruction()
        

if __name__ == "__main__":
    n = NES("smb.nes")
    print("Done")
