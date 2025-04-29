import sys
import os
# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from gameObject.gridmap import Gridmap
from gameObject.int_vector2 import IntVector2
from gameObject.snake_grid import SnakeGrid


# 打印网格内容的函数
def print_grid(grid: Gridmap) -> None:
    print("Grid:")
    print(f"Width: {grid.grid_width}, Height: {grid.grid_height}")
    print("0: Empty, 1: Snake Body, 2: Snake Head")
    print("Grid Content:")
    for i in range(grid.grid_height):
        for j in range(grid.grid_width):
            print(grid.get_cell(j, i), end=" ")
        print()

# 初始化Pygame
def init_pygame(screen_width: int, screen_height: int):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake Grid Test")
    return screen, pygame.time.Clock()

# 主循环
def main():
    screen_width, screen_height = 400, 400
    screen, clock = init_pygame(screen_width, screen_height)

    # 初始化SnakeGrid
    snake_grid = SnakeGrid(20, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新SnakeGrid状态
        snake_grid.update()
        snake_grid.fall(None)

        # 绘制网格
        screen.fill((0, 0, 0))  # 清屏为黑色
        snake_grid.draw(screen)
        pygame.display.flip()

        # 打印网格到控制台（可选）
        #print_grid(snake_grid)

        clock.tick(10)  # 限制帧率为10帧每秒

    pygame.quit()

if __name__ == "__main__":
    main()