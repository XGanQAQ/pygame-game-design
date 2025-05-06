import sys
import os
# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from gameObject.plat_grid import PlatGrid

def test_plat_grid():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("PlatGrid Test")
    clock = pygame.time.Clock()

    # Create a PlatGrid instance
    plat_grid = PlatGrid(20, 20)
    plat_grid.cell_size = 20  # Set cell size for drawing

    # Set some cells to different platform types
    plat_grid.set_platform(5, 5)
    plat_grid.set_wall(6, 5)
    plat_grid.set_bottom_layer(7, 5)
    plat_grid.set_top_layer(8, 5)

    # Main loop for testing
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the PlatGrid
        plat_grid.draw(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    test_plat_grid()
