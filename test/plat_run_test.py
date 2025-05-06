import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gameObject.plat_grid import PlatGrid

def main():
    pygame.init()
    screen_width, screen_height = 400, 400
    cell_size = 20
    grid_width, grid_height = screen_width // cell_size, screen_height // cell_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PlatGrid Test")
    clock = pygame.time.Clock()

    # Initialize PlatGrid
    plat_grid = PlatGrid(grid_width, grid_height)
    plat_grid.set_ground(5, 5)  # Set ground at (5, 5)
    plat_grid.set_platform(6, 5)  # Set platform at (6, 5)
    plat_grid.set_moving_platform(7, 5)  # Set moving platform at (7, 5)
    plat_grid.set_spike(8, 5)  # Set spike at (8, 5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Update PlatGrid
        plat_grid.update()

        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen with black
        plat_grid.draw(screen)

        pygame.display.flip()
        clock.tick(10)  # Limit to 10 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
