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

    def push(self, new_row):
        """
        Push a new row of data to the top of the grid.
        All existing data will be shifted down by one row.
        The bottom row will be discarded.
        
        Args:
            new_row (list): A list representing the new row data to be added to the top.
                          Length must match grid width.
        """
        if len(new_row) != self.grid_width:
            raise ValueError(f"New row length {len(new_row)} does not match grid width {self.grid_width}")
            
        # Shift all rows down by one
        for y in range(self.grid_height - 1, 0, -1):
            self.grid[y] = self.grid[y-1][:]
            
        # Insert the new row at the top
        self.grid[0] = new_row[:]
    
    def pop(self):
        """
        Remove and return the bottom row of the grid.
        All other rows will be shifted down, and the top row will be filled with None.
        
        Returns:
            list: The bottom row that was removed
        """
        if self.grid_height == 0:
            return None
            
        # Save the bottom row to return
        bottom_row = self.grid[-1].copy()
        
        # Shift all rows up by one
        for y in range(self.grid_height - 1, 0, -1):
            self.grid[y] = self.grid[y-1][:]
            
        # Clear the top row
        self.grid[0] = [None] * self.grid_width
        
        return bottom_row