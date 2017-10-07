from ROM import ROM
from RAM import RAM

class NES:
    rom = None
    ram = None
    cpu = None
    ppu = None
    apu = None
    
    def __init__(self, rom_name: str):
        self.rom = ROM(rom_name)
        self.ram = RAM()
        self.ram.mem_set(0x8000, bytearray(self.rom.prg_rom))

if __name__ == "__main__":
    n = NES("smb.nes")
    print("Done")
