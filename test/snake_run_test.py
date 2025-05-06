import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gameObject.snake_grid import SnakeGrid
from gameObject.gridmap import Gridmap

def main():
    pygame.init()
    screen_width, screen_height = 400, 400
    cell_size = 20
    grid_width, grid_height = screen_width // cell_size, screen_height // cell_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SnakeGrid Test")
    clock = pygame.time.Clock()

    # Initialize SnakeGrid and ItemGrid
    snake_grid = SnakeGrid(grid_width, grid_height)
    item_grid = Gridmap(grid_width, grid_height)
    item_grid.set_cell(5, 5, 50)  # Place an apple at (5, 5)

    running = True
    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Update SnakeGrid
        snake_grid.update(keys, item_grid=item_grid)

        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen with black
        snake_grid.draw(screen)
        for y in range(grid_height):
            for x in range(grid_width):
                if item_grid.get_cell(x, y) == 50:  # Draw apple
                    pygame.draw.circle(screen, (255, 0, 0), (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 3)

        pygame.display.flip()
        clock.tick(10)  # Limit to 10 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
