import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gameObject.item_grid import ItemGrid

def main():
    pygame.init()
    screen_width, screen_height = 400, 400
    cell_size = 20
    grid_width, grid_height = screen_width // cell_size, screen_height // cell_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("ItemGrid Test")
    clock = pygame.time.Clock()

    # Initialize ItemGrid
    item_grid = ItemGrid(grid_width, grid_height)
    item_grid.set_apple(5, 5)  # Set apple at (5, 5)
    item_grid.set_float_potion(6, 5)  # Set float potion at (6, 5)
    item_grid.set_invincible_star(7, 5)  # Set invincible star at (7, 5)
    item_grid.set_speed_potion(8, 5)  # Set speed potion at (8, 5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen with black
        item_grid.draw(screen)

        pygame.display.flip()
        clock.tick(10)  # Limit to 10 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
