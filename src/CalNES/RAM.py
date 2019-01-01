class ppuMEM:
    nes = None
    mode = 0
    def __init__(self, nes):
        self.nes = nes
        self.ram = bytearray(0x2000)

    def read_byte(self, address):
        address %= 0x4000
        if address < 0x2000:
            # return self.nes.mmap.read(address)
            return self.ram[address]
        elif address < 0x3F00:
            # mirror
            mode = self.nes.rom.mirroring
            return self.nes.ppu.nameTableData[mirror_address(mode, address) % 2048]
        elif address < 0x4000:
            return self.nes.ppu.readPalette(address % 32)
        else:
            print("invalid read at " + str(address))
        return 0

    def write_byte(self, address, value):
        address %= 0x4000
        if address < 0x2000:
            # self.nes.mmap.write(address, value)
            self.ram[address] = value
        elif address < 0x3f00:
            mode = self.nes.rom.mirroring
            self.nes.ppu.nameTableData[mirror_address(mode, address) % 2048] = value
        elif address < 0x4000:
            self.nes.ppu.write_palette(address % 32, value)
        else:
            print("invalid ppu memory write at " + str(address))

    def __getitem__(self, index):
        if isinstance(index, slice):
            args = [index.start, index.stop]
            if index.step:
                args.append(index.step)
            return [self.read_byte(i) for i in range(*args)]
        else:
            return self.read_byte(index)

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            args = [index.start, index.stop]
            if index.step:
                args.append(index.step)
            j = 0
            for i in range(*args):
                self.write_byte(i, value[j])
                j += 1
        else:
            self.write_byte(index, value)

mirror_lookup = [[0, 0, 1, 1], [0, 1, 0, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 2, 3]]

def mirror_address(mode, address):
    address = (address - 0x2000) % 0x1000
    table = address // 0x0400
    offset = address % 0x0400
    return 0x2000 + mirror_lookup[int(mode)][table] * 0x0400 + offset
