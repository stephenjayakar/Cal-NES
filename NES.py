from ROM import ROM
from RAM import RAM
from CPU import CPU
import time

class NES:
    rom = None
    ram = None
    cpu = None
    ppu = None
    apu = None
    
    def __init__(self, rom_name: str):
        self.rom = ROM(rom_name)
        self.ram = RAM()
        self.cpu = CPU()
        # Instructions start at 0x8000 / prg_rom
        self.ram.mem_set(0x8000, bytearray(self.rom.prg_rom))
        
        # Only runs one instruction
        self.cpu.run_instruction(self.ram)
        

if __name__ == "__main__":
    n = NES("smb.nes")
    print("Done")
