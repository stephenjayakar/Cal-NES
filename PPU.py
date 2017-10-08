from RAM import RAM
from Display import Display
import threading

class PPU():
    cpu_ram = None
    ram = None
    pixel_width, pixel_height = 256, 240
    display = None
    
    def __init__(self, cpu_ram: RAM, ppu_ram: RAM):
        self.cpu_ram = cpu_ram
        self.ram = ppu_ram
        self.display = Display()

    def tick(self):
        name = self.ram.mem_get(0x2000, 16)
        attribute = self.ram.mem_get(0x23c0, 16)

    def draw_pattern(self, offset: int):
        tile1 = combine_planes(self.ram.mem_get(offset, 16))
        # tile2 = combine_planes(self.ram.mem_get(16, 16))
        # tile3 = combine_planes(self.ram.mem_get(32, 16))
        # tile4 = combine_planes(self.ram.mem_get(48, 16))
        # tile5 = combine_planes(self.ram.mem_get(64, 16))
        # tile6 = combine_planes(self.ram.mem_get(80, 16))
        # tile7 = combine_planes(self.ram.mem_get(96, 16))
        # tile8 = combine_planes(self.ram.mem_get(112, 16))
        self.display.draw_tile(tile1, 0, 0)
        # self.display.draw_tile(tile2, 1, 0)
        # self.display.draw_tile(tile3, 0, 1)
        # self.display.draw_tile(tile4, 1, 1)
        # self.display.draw_tile(tile5, 0, 2)
        # self.display.draw_tile(tile6, 1, 2)
        # self.display.draw_tile(tile7, 0, 3)
        # self.display.draw_tile(tile8, 1, 3)
        


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
        
