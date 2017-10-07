from RAM import RAM

class PPU:
    cpu_ram = None
    ram = None
    pixel_width, pixel_height = 256, 240
    def __init__(self, cpu_ram: RAM, ppu_ram: RAM):
        self.cpu_ram = cpu_ram
        self.ram = ppu_ram

    def draw_pattern(self):
        pattern = self.ram.mem_get(0, 16)
        print("skldjflksd")
        self.combine_planes(b'\x03\x0f\x1f\x1f\x1c$&f\x00\x00\x00\x00\x1f??\x7f')

    def _combine_planes(b: bytes):
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

    def _zero_left_extend(b, n):
        """Pads a bitstring with zeros on the left and returns a bitstring of n bits.
        >>> zero_left_extend('001101', 8)
        '00001101'
        """
        if len(b) == n:
            return b
        zeros = n - len(b)
        return '0' * zeros + b

    def _str_to_lst(str):
        """Converts a bitstring to a list of ints.
        >>> str_to_lst('10010001')
        [1, 0, 0, 1, 0, 0, 0, 1]
        """
        return [int(s) for s in str]

    def _merge_bits(lst1, lst2):
        """Takes two lists of integers and merges them pairwise.
        >>> merge_bits([0, 1, 1, 0], [0, 1, 0, 1])
        [0, 3, 2, 1]
        """
        pair_add = []
        for i in range(len(lst1)):
            pair_add += [lst1[i] * 2 + lst2[i]]  # left shift lst1 bit, add to lst2 bit
        return pair_add

        
"""A tile is an 8x8 region."""
class Tile:
    pixel_width, pixel_height = 8, 8
    def __init__(self, x, y, filename):
        self.x, self.y = x, y
        self.filename = filename


"""A block is a 16x16 region containing four tiles."""
class Block:
    width, height = 2, 2
    def __init__(self, tiles):
        self.tiles = tiles

    def get_tiles(self):
        return self.tiles

    def ULtile(self):
        return self.tiles[0]

    def URtile(self):
        return self.tiles[1]

    def LLtile(self):
        return self.tiles[2]

    def LRtile(self):
        return self.tiles[3]


"""A nametable is the data structure for a background."""
class Nametable:
    width, height = 32, 30
    def __init__(self, grid):
        self.grid = grid
        self.tiles = self.all_tiles()

    """Returns a list of the tile numbers in the nametable."""
    def all_tiles(self):
        tiles = []
        for r in range(self.height):
            for c in range(self.width):
                tiles += [self.get_tile(c, r)]
        if len(tiles) != (self.width * self.height):
            return "ERROR"
        return tiles

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    """Returns an integer corresponding to a tile number."""
    def get_tile(self, col, row):
        return grid[row][col]

    """Returns the x,y position of a tile number."""
    def get_postion(self, tile):
        index = self.tiles.index(tile)
        return (index % self.width, index / self.width)
