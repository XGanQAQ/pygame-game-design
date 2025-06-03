import sys
import os
import unittest

# Add the parent directory to the path so we can import the Gridmap class
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gameObject.gridmap import Gridmap

class TestGridmap(unittest.TestCase):
    def setUp(self):
        """Set up a 3x3 grid for testing"""
        self.grid = Gridmap(3, 3)
        
    def test_initialization(self):
        """Test grid initialization"""
        self.assertEqual(self.grid.grid_width, 3)
        self.assertEqual(self.grid.grid_height, 3)
        self.assertEqual(self.grid.grid, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    
    def test_set_and_get_cell(self):
        """Test setting and getting cell values"""
        self.grid.set_cell(1, 1, 5)
        self.assertEqual(self.grid.get_cell(1, 1), 5)
        
        # Test out of bounds
        self.assertIsNone(self.grid.get_cell(5, 5))
        
    def test_clear(self):
        """Test clearing the grid"""
        self.grid.set_cell(0, 0, 1)
        self.grid.clear()
        self.assertEqual(self.grid.get_cell(0, 0), None)
    
    def test_push(self):
        """Test pushing a new row to the top"""
        # Set up initial grid
        for y in range(3):
            for x in range(3):
                self.grid.set_cell(x, y, y * 3 + x + 1)
        
        # Push a new row
        new_row = [10, 11, 12]
        self.grid.push(new_row)
        
        # Check the new grid state
        self.assertEqual(self.grid.grid[0], new_row)
        self.assertEqual(self.grid.grid[1], [1, 2, 3])
        self.assertEqual(self.grid.grid[2], [4, 5, 6])
        
    def test_pop(self):
        """Test popping the bottom row"""
        # Set up initial grid
        for y in range(3):
            for x in range(3):
                self.grid.set_cell(x, y, y * 3 + x + 1)
        
        # Pop the bottom row
        bottom_row = self.grid.pop()
        
        # Check the returned row and new grid state
        self.assertEqual(bottom_row, [7, 8, 9])
        self.assertEqual(self.grid.grid[0], [None, None, None])
        self.assertEqual(self.grid.grid[1], [1, 2, 3])
        self.assertEqual(self.grid.grid[2], [4, 5, 6])
    
    def test_push_pop_sequence(self):
        """Test a sequence of push and pop operations"""
        # Push multiple rows
        rows = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12]
        ]
        
        for row in rows:
            self.grid.push(row)
            
        # After pushing 4 rows into a 3-row grid, the first row should be gone
        self.assertEqual(self.grid.grid[0], [10, 11, 12])
        self.assertEqual(self.grid.grid[1], [7, 8, 9])
        self.assertEqual(self.grid.grid[2], [4, 5, 6])
        
        # Test pop
        self.assertEqual(self.grid.pop(), [4, 5, 6])
        self.assertEqual(self.grid.pop(), [7, 8, 9])
        self.assertEqual(self.grid.pop(), [10, 11, 12])
        
        # Grid should now be empty (filled with None)
        self.assertEqual(self.grid.grid, [[None, None, None]] * 3)

if __name__ == '__main__':
    unittest.main()
