import sys
import os
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gameObject.gridmap import Gridmap
from gameObject.snake_grid import SnakeGrid

# 打印网格内容的函数
def print_grid(grid: Gridmap) -> None:
    for i in range(grid.grid_height):
        print(" ".join(str(grid.get_cell(j, i)) for j in range(grid.grid_width)))

def test_snake_movement():
    snake = SnakeGrid(10, 10)
    keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True, pygame.K_UP: False, pygame.K_DOWN: False}
    snake.update(keys)
    print("After moving right:")
    print_grid(snake)

def test_snake_eating():
    snake = SnakeGrid(10, 10)
    item_grid = Gridmap(10, 10)
    item_grid.set_cell(6, 5, 50)  # Place an apple
    keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True, pygame.K_UP: False, pygame.K_DOWN: False}
    snake.update(keys, item_grid=item_grid)
    print("After eating apple:")
    print_grid(snake)

def test_snake_falling():
    snake = SnakeGrid(10, 10)
    plat_grid = Gridmap(10, 10)
    plat_grid.set_cell(5, 6, 10)  # Place a platform
    snake.fall(plat_grid)
    print("After falling:")
    print_grid(snake)

if __name__ == "__main__":
    test_snake_movement()
    test_snake_eating()
    test_snake_falling()