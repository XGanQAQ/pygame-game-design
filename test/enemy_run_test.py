import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gameObject.enemy_grid import EnemyGrid

def main():
    pygame.init()
    screen_width, screen_height = 400, 400
    cell_size = 20
    grid_width, grid_height = screen_width // cell_size, screen_height // cell_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("EnemyGrid Test")
    clock = pygame.time.Clock()

    # Initialize EnemyGrid
    enemy_grid = EnemyGrid(grid_width, grid_height)
    enemy_grid.set_patrol_enemy(5, 5)  # Set patrol enemy at (5, 5)
    enemy_grid.set_flying_enemy(6, 5)  # Set flying enemy at (6, 5)
    enemy_grid.set_tracking_enemy(7, 5)  # Set tracking enemy at (7, 5)

    player_pos = [10, 10]  # Simulated player position

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Update EnemyGrid
        enemy_grid.update(player_pos)

        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen with black
        enemy_grid.draw(screen)

        pygame.display.flip()
        clock.tick(10)  # Limit to 10 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
