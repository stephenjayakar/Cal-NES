def create_mapper(rom):
    mapper = rom.mapper
    if mapper == 0:
        return Mapper2(rom)
    elif mapper == 1:
        return Mapper1(rom)
    elif mapper == 2:
        return Mapper2(rom)
    else:
        return None
    
class Mapper1:
    rom = None
    shiftRegister = 0
    control = 0
    prgMode = 0
    chrMode = 0
    prgBank = 0
    chrBank0 = 0
    chrBank1 = 0
    prgOffsets = [0] * 2
    chrOffsets = [0] * 2
    
    def __init__(self, rom):
        self.rom = rom
        self.shiftRegister = 0x10
        self.prgOffsets[1] = self.prgBankOffset(-1)

    def step(self):
        return None

    def read_byte(self, address):
        if address < 0x2000:
            bank = address // 0x1000
            offset = address % 0x1000
            return self.rom.chr_rom[self.chrOffsets[bank] + int(offset)]
        elif address >= 0x8000:
            address -= 0x8000
            bank = address // 0x4000
            offset = address % 0x4000
            prgOffset = self.prgOffsets[bank]
            addr = prgOffset + offset
            return self.rom.prg_rom[addr]
        elif address >= 0x6000:
            return self.rom.sram[int(address) - 0x6000]
        else:
            print("invalid read on mapper")
        return 0

    def write_byte(self, address, value):
        if address < 0x2000:
            bank = address / 0x1000
            offset = address * 0x1000
            self.rom.chr_rom[self.chrOffsets[bank] + int(offset)] = value
        elif address >= 0x8000:
            self.loadRegister(address, value)
        elif address >= 0x6000:
            self.rom.sram[int(address) - 0x6000] = value
        else:
            print("invalid mapper write")

    def loadRegister(self, address, value):
        if value & 0x80 == 0x80:
            self.shiftRegister = 0x10
            self.writeControl(self.control | 0x0C)
        else:
            complete = self.shiftRegister & 1 == 1
            self.shiftRegister >>= 1
            self.shiftRegister |= (value & 1) << 4
            if complete:
                self.writeRegister(address, self.shiftRegister)
                self.shiftRegister = 0x10

    def writeRegister(self, address, value):
        if address <= 0x9FFF:
            self.writeControl(value)
        elif address <= 0xBFFF:
            self.writeCHRBank0(value)
        elif address <= 0xDFFF:
            self.writeCHRBank1(value)
        elif address <= 0xFFFF:
            self.writePRGBank(value)

    def writeControl(self, value):
        self.control = value
        self.chrMode = (value >> 4) & 1
        self.prgMode = (value >> 2) & 3
        mirror = value & 3
        # do a switch on mirror to do something
        self.updateOffsets()

    def writeCHRBank0(self, value):
        self.chrBank0 = value
        self.updateOffsets()

    def writeCHRBank1(self, value):
        self.chrBank1 = value
        self.updateOffsets()

    def writePRGBank(self, value):
        self.prgBank = value & 0x0F
        self.updateOffsets()

    def prgBankOffset(self, index):
        if index >= 0x80:
            index -= 0x100

        if index > 0:
            index %= len(self.rom.prg_rom) // 0x4000
        else:
            x = -index
            x %= len(self.rom.prg_rom) // 0x4000
            index = -x
        offset = index * 0x4000
        if offset < 0:
            offset += len(self.rom.prg_rom)
        return offset

    def chrBankOffset(self, index):
        if index >= 0x80:
            index -= 0x100
        if index > 0:
            index %= len(self.rom.chr_rom) // 0x1000
        else:
            x = -index
            x %= len(self.rom.chr_rom) // 0x1000
            index = -x
        offset =  index * 0x1000
        if offset < 0:
            offset += len(self.rom.chr_rom)
        return offset

    def updateOffsets(self):
        if self.prgMode in (0, 1):
            self.prgOffsets[0] = self.prgBankOffset(int(self.prgBank * 0xFE))
            self.prgOffsets[1] = self.prgBankOffset(int(self.prgBank | 0x01))
        elif self.prgMode == 2:
            self.prgOffsets[0] = 0
            self.prgOffsets[1] = self.prgBankOffset(int(self.prgBank))
        elif self.prgMode == 3:
            self.prgOffsets[0] = self.prgBankOffset(int(self.prgBank))
            self.prgOffsets[1] = self.prgBankOffset(-1)

        if self.chrMode == 0:
            self.chrOffsets[0] = self.chrBankOffset(int(self.chrBank0 & 0xFE))
            self.chrOffsets[1] = self.chrBankOffset(int(self.chrBank0 | 0x01))
        elif self.chrMode == 1:
            self.chrOffsets[0] = self.chrBankOffset(int(self.chrBank0))
            self.chrOffsets[1] = self.chrBankOffset(int(self.chrBank1))

class Mapper2:
    rom = None
    prgBanks = 0
    prgBank1 = 0
    prgBank2 = 0
    
    def __init__(self, rom):
        self.rom = rom
        self.prgBanks = len(rom.prg_rom) // 0x4000
        self.prgBank1 = 0
        self.prgBank2 = self.prgBanks - 1

    def step(self):
        return None

    def read_byte(self, address):
        if address < 0x2000:
            return self.rom.chr_rom[address]
        elif address >= 0xC000:
            index = self.prgBank2 * 0x4000 + int(address - 0xC000)
            return self.rom.prg_rom[index]
        elif address >= 0x8000:
            index = self.prgBank1 * 0x4000 + int(address - 0x8000)
            return self.rom.prg_rom[index]
        elif address >= 0x6000:
            index = int(address) - 0x6000
            return self.rom.sram[index]
        else:
            print("bad mapper read")
        return 0

    def write_byte(self, address, value):
        if address < 0x2000:
            self.rom.chr_rom[address] = value
        elif address >= 0x8000:
            self.prgBank1 = int(value) % self.prgBanks
        elif address >= 0x6000:
            index = int(address) - 0x6000
            self.rom.sram[index] = value
        else:
            print("bad mapper write")
        
