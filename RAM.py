class cpuMEM:
    nes = None
    def __init__(self, nes):
        self.nes = nes
        
    def read_byte(self, address):
        if address < 0x2000:
            return self.nes.ram[address % 0x0800]
        elif address < 0x4000:
            return self.nes.ppu.readRegister(0x2000 + address % 8)
        elif address == 0x4014:
            return self.nes.ppu.readRegister(address)
        elif address == 0x4015:
            # APU
            # return self.nes.APU.readRegister(address)
            return 0
        elif address == 0x4016:
            # read the controller 1
            return 0
        elif address == 0x4017:
            # read controller 2
            return 0
        elif address >= 0x6000:
            # mapper
            return 0
        else:
            print("uh oh")
        return 0

    def write_byte(self, address, value):
        if address < 0x2000:
            self.nes.ram[address % 0x0800] = value
        elif address < 0x4000:
            self.nes.ppu.writeRegister(0x2000 + address % 8, value)
        elif address < 0x4014:
            # apu register
            return
        elif address == 0x4014:
            self.nes.ppu.writeRegister(address, value)
        elif address == 0x4015:
            # apu thing
            print("please implement the apu")
        elif address == 0x4016:
            # write controller
            print("controllers come hither")
        elif address == 0x4017:
            # apu write register
            print("apu write register")
        elif address < 0x6000:
            # io registers
            print("io registers")
        elif address >= 0x6000:
            print("lol mappers not implemented")

class ppuMEM:
    nes = None
    mode = 0
    
    def __init__(self, nes):
        self.nes = nes

    def read_byte(self, address):
        address = address % 0x4000
        if address < 0x2000:
            return self.nes.mapper.read_byte(address)
        elif address < 0x3F00:
            print("mirror?")
        elif address < 0x4000:
            return self.nes.ppu.readPalette(address % 32)
        else:
            print("invalid read at " + str(address))
        return 0

    def write_byte(self, address, value):
        address = address % 0x4000
        if address < 0x2000:
            self.nes.mapper.write(address, value)
        elif address < 0x3f00:
            print("mirror write")
        elif address < 0x4000:
            self.nes.ppu.writePalette(address % 32, value)
        else:
            print("invalid ppu memory write at " + str(address))
            
# class RAM:
#     memory = None
    
#     def __init__(self):
#         self.memory = bytearray(0x10000)

#     def mem_set(self, offset: int, data: bytearray) -> None:
#         length = len(data)
#         self.memory[offset:offset + length] = data

#     # Read from start to length in bytes
#     def mem_get(self, offset: int, length: int) -> bytes:
#         # max_index = offset + length
#         # if max_index < len(self.memory):
#         return bytes(self.memory[offset:offset + length])

#     def read_byte(self, offset: int) -> int:
#         return self.memory[offset]

#     def write_byte(self, offset: int, value: int) -> None:
#         self.memory[offset] = value
