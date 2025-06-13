from enum import Enum
from shutil import move
from typing import List, Dict, Optional, Union
from pygame import Vector2
from gameObject.gridmap import Gridmap
from gameObject.int_vector2 import IntVector2
from blinker import Signal  # 引入 blinker 信号库
from collections import deque
from gameObject.snake import Snake
from gameObject.snake import CollisionStatus
import tools
import pygame


class SnakeGrid(Gridmap):
    def __init__(self, width, height, cell_size=20):
        super().__init__(width, height)

        self.snake:Snake = None  

        # Art Sources
        self.cell_size = cell_size
        self.snake_head_image = None
        self.snake_body_image = None
        self.snake_tail_image = None

        self.direction = IntVector2(-1, 0)

        self.set_snake_art(tools.load_image("snake_head.png"), tools.load_image("snake_body.png"), tools.load_image("snake_tail.png"))

        self.on_snake_get_hurt_animation_timer = 0
        self.on_snake_get_hurt_animation_duration = 0.2  # 动画持续时间: 默认 0.2秒，在后面会被初始化的和蛇的受伤间隔时间一致
        self.is_snake_get_hurt_animation_end = False
    
    def event(self, event):
        """
        Handle events for the snake grid
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction = IntVector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.direction = IntVector2(1, 0)
            elif event.key == pygame.K_UP:
                self.direction = IntVector2(0, -1)
            elif event.key == pygame.K_DOWN:
                self.direction = IntVector2(0, 1)

    def update(self, keys, delta_time, plat_grid=None, item_grid=None, enemy_grid=None):
        self.snake.update(delta_time, self.direction, self, plat_grid, item_grid, enemy_grid)
        self.__snake_map_grid(self.snake)

        # 蛇受伤动画计时器
        if self.on_snake_get_hurt_animation_timer:
            self.on_snake_get_hurt_animation_timer -= delta_time  # delta_time 是秒，转换为毫秒
            if self.on_snake_get_hurt_animation_timer <= 0:
                self.on_snake_get_hurt_animation_timer = 0
                self.is_snake_get_hurt_animation_end = True

        if self.is_snake_get_hurt_animation_end:
            self.on_snake_get_hurt_animation_end(self.snake)
            self.is_snake_get_hurt_animation_end = False

    def draw(self, screen):
        """
        Draw the snake on the screen with special tail color
        """
        # First draw all body parts
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
                elif cell_value == 32:  # Snake tail
                    if self.snake_tail_image:
                        screen.blit(self.snake_tail_image, (j * self.cell_size, i * self.cell_size))
                    else:
                        pygame.draw.rect(screen, (0, 150, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
        
    def roll(self):
        self.snake.roll()
        self.__snake_map_grid(self.snake)

    def init_snake(self, item_grid):
        self.snake = Snake(self.__grid_map_snake(), item_grid)
        self.snake.snake_get_hurt_signal.connect(self.on_snake_get_hurt_animation_begin)
        self.on_snake_get_hurt_animation_duration = self.snake.get_hurt_gap_time

    def set_snake_is_enable_falling(self, is_enable: bool):
        self.snake.is_enable_fall = is_enable

    def set_move_speed(self, speed: float):
        """
        设置蛇的移动速度
        :param speed: 移动速度
        """
        self.snake.move_speed = speed
    
    def set_fall_speed(self, speed: float):
        """
        设置蛇的掉落速度
        :param speed: 掉落速度
        """
        self.fall_speed = speed

    def set_snake_art(self, head_image: pygame.Surface = None, body_image: pygame.Surface = None, tail_image: pygame.Surface = None):
        """
        设置蛇的美术资源
        :param head_image: 蛇头图片，必须是pygame.Surface对象
        :param body_image: 蛇身图片，必须是pygame.Surface对象
        :param tail_image: 蛇尾图片，必须是pygame.Surface对象。如果为None，则使用body_image或默认颜色
        """
        if head_image is not None:
            if not isinstance(head_image, pygame.Surface):
                raise TypeError("head_image must be a pygame.Surface object")
            self.snake_head_image = head_image
            
        if body_image is not None:
            if not isinstance(body_image, pygame.Surface):
                raise TypeError("body_image must be a pygame.Surface object")
            self.snake_body_image = body_image
            
        if tail_image is not None:
            if not isinstance(tail_image, pygame.Surface):
                raise TypeError("tail_image must be a pygame.Surface object")
            self.snake_tail_image = tail_image
    
    def __snake_map_grid(self, snake: Snake):
        self.clear()
        for pos in snake.snake_body:
            self.set_cell(pos.x, pos.y, 30)
        self.set_cell(snake.snake_head.x, snake.snake_head.y, 31)
        if snake.snake_length > 1:
            self.set_cell(snake.snake_tail.x, snake.snake_tail.y, 32)
        
    def __grid_map_snake(self)->deque[IntVector2]:
        #遍历grid，找到蛇的身体
        snake_body = deque()
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.get_cell(x, y) == 30 or self.get_cell(x, y) == 31 or self.get_cell(x, y) == 32:
                    snake_body.append(IntVector2(x, y))
        return snake_body
    
    def on_snake_get_hurt_animation_begin(self, sender, **kwargs):
        """
        蛇受伤动画
        :param snake: 蛇对象
        """
        # 这里可以添加蛇受伤时的动画逻辑
        self.snake_head_image.set_alpha(128)  # 例如将蛇头半透明显示
        self.snake_body_image.set_alpha(128)  # 蛇身半透明显示
        self.snake_tail_image.set_alpha(128)  # 蛇尾半透明显示
        self.on_snake_get_hurt_animation_timer = self.on_snake_get_hurt_animation_duration

    def on_snake_get_hurt_animation_end(self, sender, **kwargs):
        """
        蛇受伤动画结束
        :param snake: 蛇对象
        """
        # 这里可以添加蛇受伤动画结束后的逻辑
        self.snake_head_image.set_alpha(255)  # 恢复蛇头不透明
        self.snake_body_image.set_alpha(255)
        self.snake_tail_image.set_alpha(255)
        self.on_snake_get_hurt_animation_timer = 0