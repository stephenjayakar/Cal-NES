from RAM import RAM

class PPU:
    cpu_ram = None
    ram = None
    xpixels, ypixels = 256, 240
    def __init__(self, cpu_ram: RAM, ppu_ram: RAM):
        self.cpu_ram = cpu_ram
        self.ram = ppu_ram


"""A tile is an 8x8 region."""
class Tile:
    xpixels, ypixels = 8, 8
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