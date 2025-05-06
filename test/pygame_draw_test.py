import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Draw Test")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
BROWN = (139, 69, 19)
YELLOW = (255, 223, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill(BLUE)

    # Draw ground
    pygame.draw.rect(screen, LIGHT_GREEN, (0, screen_height // 2, screen_width, screen_height // 2))

    # Draw sun
    pygame.draw.circle(screen, YELLOW, (700, 100), 50)

    # Draw house
    pygame.draw.rect(screen, RED, (300, 300, 200, 200))  # House base
    pygame.draw.polygon(screen, GRAY, [(300, 300), (500, 300), (400, 200)])  # Roof

    # Draw tree
    pygame.draw.rect(screen, BROWN, (150, 350, 30, 150))  # Trunk
    pygame.draw.circle(screen, GREEN, (165, 330), 50)  # Leaves

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
