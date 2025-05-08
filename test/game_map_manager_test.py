import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gameObject.game_map_manager import GameMapManager

def main():
    pygame.init()
    screen_width, screen_height = 800, 800
    cell_size = 20
    grid_width, grid_height = screen_width // cell_size, screen_height // cell_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("GameMapManager Test")
    clock = pygame.time.Clock()

    # Initialize GameMapManager
    game_map_manager = GameMapManager(grid_width, grid_height)

    # Add some initial objects
    for i in range(grid_width-5):
        game_map_manager.plat_grid.set_ground(i, 25)
    game_map_manager.item_grid.set_apple(6, 10)
    game_map_manager.enemy_grid.set_patrol_enemy(7, 10)

    game_map_manager.is_rolling = True  # Start rolling
    game_map_manager.set_snake_is_enable_falling(True)  # Enable falling for the snake

    running = True
    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Update the map
        game_map_manager.update(keys)

        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen with black
        game_map_manager.draw(screen)

        pygame.display.flip()
        clock.tick(10)  # Limit to 10 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
