from typing import List, Dict, Optional, Union
from pygame import Vector2
from gameObject.gridmap import Gridmap
from gameObject.int_vector2 import IntVector2

import pygame

class SnakeGrid(Gridmap):
    # 网格 1代表蛇身，2代表蛇头，0代表空格
    def __init__(self, width, height):
        super().__init__(width, height)
        self.snake_body_length: int = 0
        self.direction = IntVector2(1, 0)  # 蛇的移动方向，初始向右移动
        self.snake_head = IntVector2(0, 0)  # 蛇头的坐标，存储当个IntVector2
        self.snake_body = List[IntVector2]  # 蛇身的坐标列表,存储多个IntVector2

        self.snake_head_image = None
        self.snake_body_image = None

        self.cell_size = 20  # 每个格子的大小

        self.set_snake_head(0, 0)  # 设置蛇头初始位置

    def update(self):
        # 玩家移动更新
        # 定义方向向量
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction = IntVector2(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.direction = IntVector2(1, 0)
        if keys[pygame.K_UP]:
            self.direction = IntVector2(0, -1)
        if keys[pygame.K_DOWN]:
            self.direction = IntVector2(0, 1)

        self.move_snake(self.direction)  # 移动蛇

    def draw(self, screen):
        # 绘制蛇
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.get_cell(j, i) == 1:
                    # 绘制蛇身
                    if self.snake_body_image:
                        screen.blit(self.snake_body_image, (j * self.cell_size, i * self.cell_size))
                    else:
                        pygame.draw.rect(screen, (0, 255, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                elif self.get_cell(j, i) == 2:
                    # 绘制蛇头
                    if self.snake_head_image:
                        screen.blit(self.snake_head_image, (j * self.cell_size, i * self.cell_size))
                    else:
                        pygame.draw.rect(screen, (0, 200, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def set_snake_head(self, x, y):
        old_head = self.snake_head  # 备份原蛇头位置
        new_head = IntVector2(x, y)  # 新蛇头位置
        self.set_cell(old_head.x, old_head.y, 0)  # 清空原位置
        self.set_cell(new_head.x, new_head.y, 2)  # 设置蛇头
        self.snake_head = IntVector2(x, y)  # 刷新

    def get_snake_head(self):
        return self.snake_head

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def move_snake(self, direction: IntVector2) -> None:
        """
        移动蛇
        :return: None
        """
        # 更新蛇头位置
        new_head = self.snake_head + direction
        # 检查蛇头是否碰到边界
        if new_head.x < 0 or new_head.x >= self.grid_width or new_head.y < 0 or new_head.y >= self.grid_height:
            # 蛇头碰到边界，游戏结束
            print("Game Over!")
            return
        # 检查蛇头是否碰到自己
        if self.get_cell(int(new_head.x), int(new_head.y)) == 1:
            pass
        self.set_snake_head(int(new_head.x), int(new_head.y))  # 更新蛇头位置

        # 更新蛇身位置
        if self.snake_body_length > 0:
            # 如果蛇身长度大于0，则更新蛇身位置
            for i in range(self.snake_body_length):
                if self.get_cell(int(new_head.x), int(new_head.y)) == 1:
                    # 蛇头碰到蛇身，游戏结束
                    print("Game Over!")
                    return
                # 更新蛇身位置
                self.set_cell(int(new_head.x), int(new_head.y), 1)

    def check_fall(self, plat_grid: Gridmap) -> bool:
        """
        检查蛇头是否掉落
        如果蛇头的下方没有平台，则掉落
        :param plat_grid: 平台地图
        :return: True表示掉落，False表示没有掉落
        """
        # 遍历蛇的下方,如果下方有平台，则不掉落
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.get_cell(j, i) == 2 or self.get_cell(j, i) == 1:
                    if plat_grid.get_cell(j, i + 1) == 1:
                        return False
        return True

    def fall(self, plat_grid: Gridmap) -> None:
        if plat_grid is None:
            return
        else:
            if self.check_fall(plat_grid):
                # 蛇掉落
                for i in range(self.grid_height):
                    for j in range(self.grid_width):
                        if self.get_cell(j, i) == 2:
                            self.set_cell(j, i, 0)
                            self.set_cell(j, i + 1, 2)
                        elif self.get_cell(j, i) == 1:
                            self.set_cell(j, i, 0)
                            self.set_cell(j, i + 1, 1)
