from typing import List, Dict, Optional, Union
from pygame import Vector2
from gameObject.gridmap import Gridmap
from gameObject.int_vector2 import IntVector2

import pygame

class SnakeGrid(Gridmap):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.snake_body_length: int = 0
        self.direction = IntVector2(1, 0)  # Initial direction: right
        self.snake_head = IntVector2(width // 2, height // 2)  # Start at center
        self.snake_body: List[IntVector2] = []
        self.snake_head_image = None
        self.snake_body_image = None
        self.cell_size = 20
        self.set_snake_head(self.snake_head.x, self.snake_head.y)

    def update(self, keys, item_grid=None, enemy_grid=None):
        if keys[pygame.K_LEFT]:
            self.direction = IntVector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.direction = IntVector2(1, 0)
        elif keys[pygame.K_UP]:
            self.direction = IntVector2(0, -1)
        elif keys[pygame.K_DOWN]:
            self.direction = IntVector2(0, 1)

        self.move_snake(self.direction, item_grid, enemy_grid)

    def draw(self, screen):
        """

        """
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                cell_value = self.get_cell(j, i)
                if cell_value == 30:  # Snake body
                    if self.snake_body_image:
                        screen.blit(self.snake_body_image, (j * self.cell_size, i * self.cell_size))
                    else:
                        pygame.draw.rect(screen, (0, 255, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                elif cell_value == 31:  # Snake head
                    if self.snake_head_image:
                        screen.blit(self.snake_head_image, (j * self.cell_size, i * self.cell_size))
                    else:
                        pygame.draw.rect(screen, (0, 200, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def set_snake_head(self, x, y):
        old_head = self.snake_head
        new_head = IntVector2(x, y)
        # 因为在蛇头单个移动的时候，蛇身的最后一个位置会被清除，所以这里需要判断一下
        if(self.get_cell(old_head.x, old_head.y) != 30):
            self.set_cell(old_head.x, old_head.y, 0)
        self.set_cell(new_head.x, new_head.y, 31)
        self.snake_head = new_head

    def move_snake(self, direction: IntVector2, item_grid=None, enemy_grid=None):
        new_head = self.snake_head + direction

        # Check boundaries
        if new_head.x < 0 or new_head.x >= self.grid_width or new_head.y < 0 or new_head.y >= self.grid_height:
            print("Game Over! Hit boundary.")
            return

        # Check self-collision
        if self.get_cell(new_head.x, new_head.y) == 30:
            print("Game Over! Self-collision.")
            return

        # Check item collision
        if item_grid and item_grid.get_cell(new_head.x, new_head.y) == 50:  # Apple
            self.add_snake_body()
            item_grid.set_cell(new_head.x, new_head.y, 0)

        # Check enemy collision
        if enemy_grid and enemy_grid.get_cell(new_head.x, new_head.y) > 0:
            print("Game Over! Hit enemy.")
            return

        # Update snake body
        if self.snake_body_length > 0:
            tail = self.snake_body.pop()
            self.set_cell(tail.x, tail.y, 0)
            self.snake_body.insert(0, self.snake_head)
            self.set_cell(self.snake_body[0].x, self.snake_body[0].y, 30)

        # Update snake head
        self.set_snake_head(new_head.x, new_head.y)

    def add_snake_body(self):
        if self.snake_body_length == 0:
            new_tail = self.snake_head - self.direction
        else:
            last_body = self.snake_body[-1]
            second_last_body = self.snake_body[-2] if len(self.snake_body) > 1 else self.snake_head
            new_tail = last_body + (last_body - second_last_body)
        self.snake_body.append(new_tail)
        self.set_cell(new_tail.x, new_tail.y, 30)
        self.snake_body_length += 1

    def fall(self, plat_grid: Gridmap):
        if not plat_grid:
            return
        for segment in [self.snake_head] + self.snake_body:
            if segment.y + 1 < self.grid_height and plat_grid.get_cell(segment.x, segment.y + 1) == 0:
                self.set_cell(segment.x, segment.y, 0)
                segment.y += 1
                self.set_cell(segment.x, segment.y, 31 if segment == self.snake_head else 30)
