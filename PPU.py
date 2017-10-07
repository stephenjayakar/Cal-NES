class PPU:
    def __init__(self):
        print("Picture Processing Unit")

"""A nametable is the data structure for a background."""
class nametable:
    def __init__(self, grid):
        self.grid = grid
        self.width, self.height = len(grid[0]), len(grid)
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