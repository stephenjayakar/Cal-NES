from RAM import RAM
from Display import Display
import random
import pygame


class PPU:
    nes = None
    ram = None
    cycle = 0 # 0-340
    scanline = 0 # 0-261, 0-239=visible, 240=post, 241-260=vblank, 261=pre
    frame = 0 # frame counter

    paletteData = []
    nameTableData = []
    oamData = []
    # not sure what these two do
    front = None
    back = None

    # PPU Registers
    v = 0 # current vram address, 15b
    t = 0 # temp vram address, 15b
    x = 0 # fine x scroll 3b
    w = 0 # write toggle 1b
    f = 0 # even/odd frame flag 1b

    register = 0 # byte? not sure what this is for

    # nmi flags, what is this lol
    nmiOccured = False
    nmiOutput = False
    nmiPrevious = False
    nmiDelay = 0 # 8b

    # background temp vars, maybe make these locals
    nameTableByte = 0 #      byte
    attributeTableByte = 0 #  byte
    lowTileByte = 0 #        byte
    highTileByte = 0 #      byte
    tileData = 0 #           uint64

    # sprite temporary variables
    spriteCount = 0 #      int
    spritePatterns = [] #   [8]uint32
    spritePositions = [] # [8]byte
    spritePriorities = [] # [8]byte
    spriteIndexes = [] #    [8]byte

    # $2000 PPUCTRL
    flagNameTable = 0 #       byte // 0: $2000; 1: $2400; 2: $2800; 3: $2C00
    flagIncrement = 0 #      byte // 0: add 1; 1: add 32
    flagSpriteTable = 0 #     byte // 0: $0000; 1: $1000; ignored in 8x16 mode
    flagBackgroundTable = 0 # byte // 0: $0000; 1: $1000
    flagSpriteSize = 0 #      byte // 0: 8x8; 1: 8x16
    flagMasterSlave = 0 #    byte // 0: read EXT; 1: write EXT

    # $2001 PPUMASK
    flagGrayscale = 0 #          byte // 0: color; 1: grayscale
    flagShowLeftBackground = 0# byte // 0: hide; 1: show
    flagShowLeftSprites = 0 #    byte // 0: hide; 1: show
    flagShowBackground = 0 #    byte // 0: hide; 1: show
    flagShowSprites = 0 #       byte // 0: hide; 1: show
    flagRedTint = 0 #            byte // 0: normal; 1: emphasized
    flagGreenTint = 0 #         byte // 0: normal; 1: emphasized
    flagBlueTint = 0 #          byte // 0: normal; 1: emphasized

    # $2002 PPUSTATUS
    flagSpriteZeroHit = 0 #   byte
    flagSpriteOverflow = 0 # byte

    # $2003 OAMADDR
    oamAddress = 0 # byte

    # $2007 PPUDATA
    bufferedData = 0 # byte // for buffered reads

    def __init__(self, nes, ram):
        self.nes = nes
        self.ram = ram
        self.display = Display()

    def reset(self):
        self.cycle = 340
        self.scanline = 240
        self.frame = 0
        self.writeControl(0)
        self.writeMask(0)
        self.writeOAMAddress(0)

    def readPalette(self, address):
	if address >= 16 and address % 4 == 0:
	    address -= 16
	return ppu.paletteData[address]
    
    def writePalette(address, value):
	if address >= 16 and address % 4 == 0:
	    address -= 16
	ppu.paletteData[address] = value

    def readRegister(self, address):
        if address == 0x2002:
            return self.readStatus()
        if address == 0x2004:
            return self.readOAMData()
        if address == 0x2007:
            return self.readData()
        return 0

    # consider rewriting this with hashing
    def writeRegister(address, value):
        self.register = value
        if address == 0x2000:
	    self.writeControl(value)
	if address == 0x2001:
	    self.writeMask(value)
	if address == 0x2003:
	    self.writeOAMAddress(value)
	if address == 0x2004:
	    self.writeOAMData(value)
	if address == 0x2005:
	    self.writeScroll(value)
	if address == 0x2006:
	    self.writeAddress(value)
	if address == 0x2007:
	    self.writeData(value)
	if address == 0x4014:
	    self.writeDMA(value)

    def writeControl(self, ctrl: int):
        self.flagNameTable = ctrl & 3
        self.flagIncrement = (ctrl >> 2) & 1
        self.flagSpriteTable = (ctrl >> 3) & 1
        self.flagBackgroundTable = (ctrl >> 4) & 1
        self.flagSpriteSize = (ctrl >> 5) & 1
        self.flagMasterSlave = (ctrl >> 6) & 1
        self.nmiOutput = ((ctrl >> 7) & 1) == 1
        self.nmiChange()
        self.t = (self.t & 0xF3FF) | ((ctrl & 0x03) << 10)

    def writeMask(self, mask: int):
        self.flagGrayscale = mask & 1
        self.flagShowLeftBackground = (mask >> 1) & 1
	self.flagShowLeftSprites = (mask >> 2) & 1
	self.flagShowBackground = (mask >> 3) & 1
	self.flagShowSprites = (mask >> 4) & 1
	self.flagRedTint = (mask >> 5) & 1
	self.flagGreenTint = (mask >> 6) & 1
	self.flagBlueTint = (mask >> 7) & 1

    def readStatus(self):
        result = self.register & 0x1F
	result |= self.flagSpriteOverflow << 5
	result |= self.flagSpriteZeroHit << 6
	if self.nmiOccurred:
	    result |= 1 << 7
	self.nmiOccurred = false
	self.nmiChange()
	self.w = 0
	return result
        
    def writeOAMAddress(self, oam: int):
        self.oamAddress = oam

    def writeScroll(value):
        if self.w == 0:
            self.t = (self.t & 0xFFE0) | (value >> 3)
            self.x = value & 0x07
            self.w = 1
        else:
            self.t = (self.t & 0x8FFF) | ((value & 0x07) << 12)
            self.t = (self.t & 0xFC1F) | ((value & 0xF8) << 2)
            self.w = 0

    def writeAddress(value):
        if self.w == 0:
            self.t = (self.t & 0x80FF) | ((value & 0x3F) << 8)
            self.w = 1
        else:
            self.t = (self.t & 0xFF00) | value
            self.v = self.t
            self.w = 0

    def readData(self):
        value = self.Read(self.v)
        
    def nmiChange(self):
        nmi = self.nmiOutput and self.nmiOccured
        if nmi and !self.nmiPrevious:
            # uh there's apparently a long delay here
            self.nmiDelay = 15
        self.nmiPrevious = nmi


# TODO: This definitely doesn't work
'''
class PPU:
    cpu_ram = None
    ram = None
    pixel_width, pixel_height = 256, 240
    display = None
    current_nametable = None
    nametable_index = 0
    
    def __init__(self, cpu_ram: RAM, ppu_ram: RAM):
        self.cpu_ram = cpu_ram
        self.ram = ppu_ram
        self.display = Display()

    # A tile is 16 bytes
    def tick(self):
        # PPU_CTRL = self.cpu_ram.mem_get(0x2000, 8)
        # ppu_ctrl_r1, ppu_ctrl_r2, ppu_status, ppu_spr_addr, ppu_spr_data, ppu_scroll_reg, ppu_address, ppu_data = PPU_CTRL
        # ppu_status = ppu_status | 0x80
        # self.cpu_ram.mem_set(0x2002, bytes([ppu_status]))        
        i = self.nametable_index
        if not self.current_nametable:
            self.current_nametable = self.ram.mem_get(0x2400, 960)
            self.nametable_index = 0
        if i < len(self.current_nametable):
            tile = self.ram.mem_get(self.current_nametable[i] * 64, 16)
            tile = combine_planes(tile)
            self.display.draw_tile(tile, i % 16, i // 16)
            self.nametable_index += 1
        
    def draw_pattern(self, offset: int):
        tile1 = combine_planes(self.ram.mem_get(offset, 16))
        self.display.draw_tile(tile1, 0, 0)

    def update_display(self):
        pygame.display.update()


def combine_planes(b: bytes):
    """Takes a string of bytes for two planes and returns one merged list.
        >>> combine_planes(b'\x03\x0f\x1f\x1f\x1c$&f\x00\x00\x00\x00\x1f??\x7f')
        [0, 0, 0, 0, 0, 0, 2, 2,
         0, 0, 0, 0, 2, 2, 2, 2,
         0, 0, 0, 2, 2, 2, 2, 2,
         0, 0, 0, 2, 2, 2, 2, 2,
         0, 0, 0, 3, 3, 3, 1, 1,
         0, 0, 3, 1, 1, 3, 1, 1,
         0, 0, 3, 1, 1, 3, 3, 1,
         0, 3, 3, 1, 1, 3, 3, 1]
        """
    b_bin = [zero_left_extend(bin(x)[2:], 8) for x in b]  # bitstring zero-padded
    plane1_splice = b_bin[0:len(b_bin) // 2]
    plane2_splice = b_bin[len(b_bin) // 2:]
    plane1 = [str_to_lst(s) for s in plane1_splice]  # lists of bits
    plane2 = [str_to_lst(s) for s in plane2_splice]

    merge_all = []
    for i in range(len(plane1)):
        merge_all += merge_bits(plane1[i], plane2[i])
    return merge_all

def zero_left_extend(b, n):
    """Pads a bitstring with zeros on the left and returns a bitstring of n bits.
        >>> zero_left_extend('001101', 8)
        '00001101'
    """
    if len(b) == n:
        return b
    zeros = n - len(b)
    return '0' * zeros + b

def str_to_lst(str):
    """Converts a bitstring to a list of ints.
    >>> str_to_lst('10010001')
    [1, 0, 0, 1, 0, 0, 0, 1]
    """
    return [int(s) for s in str]

def merge_bits(lst1, lst2):
    """Takes two lists of integers and merges them pairwise.
    >>> merge_bits([0, 1, 1, 0], [0, 1, 0, 1])
    [0, 3, 2, 1]
    """
    pair_add = []
    for i in range(len(lst1)):
        pair_add += [lst1[i] * 2 + lst2[i]]  # left shift lst1 bit, add to lst2 bit
    return pair_add
        
'''
