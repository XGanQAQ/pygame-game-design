
class Gridmap:
    def __init__(self, width, height):
        self.grid_width = width
        self.grid_height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def set_cell(self, x, y, value):
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.grid[y][x] = value

    def get_cell(self, x, y):
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            return self.grid[y][x]
        return None

    def clear(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                self.grid[y][x] = None