from typing import List, Dict, Optional, Union
from pygame import Vector2
from gameObject.gridmap import Gridmap
from gameObject.int_vector2 import IntVector2
from blinker import Signal  # 引入 blinker 信号库

import pygame

class SnakeGrid(Gridmap):
    def __init__(self, width, height, cell_size=20):
        super().__init__(width, height)

        # Singnal
        self.snake_init_signal = Signal()  # 蛇初始化信号
        self.snak_dead_signal = Signal()  # 蛇死亡信号
        self.snake_grow_signal = Signal()  # 蛇生长信号

        # Body Length
        self.snake_body_length: int = 0

        # Position and direction
        self.direction = IntVector2(1, 0)  # Initial direction: right
        self.snake_head = IntVector2(width // 2, height // 2)  # Start at center
        self.snake_body: List[IntVector2] = []

        # Move Speed
        self.move_speed = 300  # Speed of the snake movement
        self.move_speed_buffer = 0
        self.move_speed_buffer_max = 100  # Speed buffer to control the speed of the snake
        
        # Falling speed
        self.fall_speed = 600  # 掉落速度
        self.fall_speed_buffer = 0
        self.fall_speed_buffer_max = 100  # 掉落速度缓冲区最大值

        # Art Sources
        self.cell_size = cell_size
        self.snake_head_image = None
        self.snake_body_image = None

        # Move and falling states
        self.is_enable_falling = False  # 是否允许掉落
        self.is_falling = False  # 是否正在掉落

        # Float effect
        self.float_effect_duration = 5000  # 浮空效果持续时间 (毫秒)
        self.float_effect_timer = 0  # 浮空效果计时器
        self.is_floating_effect_active = False # 浮空效果是否激活

        # Invincible effect
        self.invincible_effect_duration = 5000  # 无敌效果持续时间 (毫秒)
        self.invincible_effect_timer = 0  # 无敌效果计时器
        self.is_invincible_effect_active = False # 无敌效果是否激活

        # Speed boost effect
        self.speed_boost_effect_duration = 5000  # 加速效果持续时间 (毫秒)
        self.speed_boost_effect_timer = 0  # 加速效果计时器
        self.is_speed_boost_active = False  # 加速效果是否激活
        self.speed_boost_multiplier = 0.5  # 速度增加50%
        self.original_move_speed = self.move_speed # 存储原始移动速度

        # 
        #self.__set_snake_head(self.snake_head.x, self.snake_head.y)

    def update(self, keys, delta_time, plat_grid=None, item_grid=None, enemy_grid=None):
        if keys[pygame.K_LEFT]:
            self.direction = IntVector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.direction = IntVector2(1, 0)
        elif keys[pygame.K_UP]:
            self.direction = IntVector2(0, -1)
        elif keys[pygame.K_DOWN]:
            self.direction = IntVector2(0, 1)

        # 更新浮空效果计时器
        if self.is_floating_effect_active:
            self.float_effect_timer -= delta_time * 1000  # delta_time 是秒，转换为毫秒
            if self.float_effect_timer <= 0:
                self.is_floating_effect_active = False
                self.is_enable_falling = True  # 效果结束，恢复允许掉落
                self.float_effect_timer = 0

        # 更新无敌效果计时器
        if self.is_invincible_effect_active:
            self.invincible_effect_timer -= delta_time * 1000  # delta_time 是秒，转换为毫秒
            if self.invincible_effect_timer <= 0:
                self.is_invincible_effect_active = False
                self.invincible_effect_timer = 0

        # 更新加速效果计时器
        if self.is_speed_boost_active:
            self.speed_boost_effect_timer -= delta_time * 1000  # delta_time 是秒，转换为毫秒
            if self.speed_boost_effect_timer <= 0:
                self.is_speed_boost_active = False
                self.move_speed = self.original_move_speed  # 恢复原始速度
                self.speed_boost_effect_timer = 0

        # 如果允许掉落，则开启掉落
        if self.is_enable_falling:
            self.__fall(delta_time, plat_grid)

        # 如果不处于掉落状态并且满足移动需求逻辑，则可以移动蛇
        if not self.is_falling and self.__move_speed_logic(delta_time):
            self.__move_snake(self.direction, plat_grid, item_grid, enemy_grid)

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

    def set_move_speed(self, speed: float):
        """
        设置蛇的移动速度
        :param speed: 移动速度
        """
        self.move_speed = speed
    
    def set_fall_speed(self, speed: float):
        """
        设置蛇的掉落速度
        :param speed: 掉落速度
        """
        self.fall_speed = speed

    # 放置头的位置
    # 但是仅仅放置了头，没有把身体一同调整
    # 所有仅仅适用于初始化放置头
    def set_snake_head(self, x, y):
        old_head = self.snake_head
        new_head = IntVector2(x, y)
        # 因为在蛇头单个移动的时候，蛇身的最后一个位置会被清除，所以这里需要判断一下
        if(self.get_cell(old_head.x, old_head.y) != 30):
            self.set_cell(old_head.x, old_head.y, 0)
        self.set_cell(new_head.x, new_head.y, 31)
        self.snake_head = new_head

    def __move_speed_logic(self, delta_time):
        """
        控制蛇的移动速度
        """
        self.move_speed_buffer += self.move_speed * delta_time
        # 如果速度缓冲区达到最大值，则返回True，表示可以移动
        if self.move_speed_buffer >= self.move_speed_buffer_max:
            self.move_speed_buffer = self.move_speed_buffer % self.move_speed_buffer_max  # 重置速度缓冲区
            return True
        return False

    def __move_snake(self, direction: IntVector2, plat_grid=None, item_grid=None, enemy_grid=None):
        new_head = self.snake_head + direction

        # Check boundaries
        if new_head.x < 0 or new_head.x >= self.grid_width or new_head.y < 0 or new_head.y >= self.grid_height:
            print("Game Over! Hit boundary.")
            return

        # Check self-collision
        if self.get_cell(new_head.x, new_head.y) == 30:
            print("Game Over! Self-collision.")
            return

        # Check platform collision
        if plat_grid:
            value = plat_grid.get_cell(new_head.x, new_head.y)
            if value == 0: # Empty space
                pass
            elif value == 10: # Platform
                return
            elif value == 20: # 尖刺
                if not self.is_invincible_effect_active:
                    self.snak_dead_signal.send(self)  # 发送蛇死亡信号
                    print("Game Over! Hit 尖刺.")
                    return

        # Check item collision
        if item_grid:
            value = item_grid.get_cell(new_head.x, new_head.y)
            if value == 50: # Apple
                self.__add_snake_body()
                item_grid.set_cell(new_head.x, new_head.y, 0)
            if value == 51: # Float potion
                self.is_enable_falling = False
                self.is_floating_effect_active = True
                self.float_effect_timer = self.float_effect_duration
                item_grid.set_cell(new_head.x, new_head.y, 0) # 移除药水
            if value == 52: # Invincible star
                self.is_invincible_effect_active = True
                self.invincible_effect_timer = self.invincible_effect_duration
                item_grid.set_cell(new_head.x, new_head.y, 0) # 移除星星
            if value == 53: # Speed boost potion
                if not self.is_speed_boost_active: # 只有在加速效果未激活时才保存原始速度
                    self.original_move_speed = self.move_speed
                self.is_speed_boost_active = True
                self.speed_boost_effect_timer = self.speed_boost_effect_duration
                self.move_speed = self.original_move_speed * (1 + self.speed_boost_multiplier)
                item_grid.set_cell(new_head.x, new_head.y, 0) # 移除药水

        # Check enemy collision
        if enemy_grid:
            value = enemy_grid.get_cell(new_head.x, new_head.y)
            if value == 40:
                if not self.is_invincible_effect_active:
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

    def __add_snake_body(self):
        if self.snake_body_length == 0:
            new_tail = self.snake_head - self.direction
        else:
            last_body = self.snake_body[-1]
            second_last_body = self.snake_body[-2] if len(self.snake_body) > 1 else self.snake_head
            new_tail = last_body + (last_body - second_last_body)
        self.snake_body.append(new_tail)
        self.set_cell(new_tail.x, new_tail.y, 30)
        self.snake_body_length += 1

    def __fall(self, delta_time, plat_grid: Gridmap):
        # 控制掉落速度
        self.fall_speed_buffer += self.fall_speed * delta_time
        if self.fall_speed_buffer < self.fall_speed_buffer_max:
            return  # 缓冲未满，不执行掉落

        # 重置缓冲区
        self.fall_speed_buffer %= self.fall_speed_buffer_max

        self.is_falling = False

        # 如果没有平台网格，则不进行掉落
        if not plat_grid:
            return
        
        # 检测所有蛇头和蛇身下方是否有平台
        for segment in [self.snake_head] + self.snake_body:
            value = plat_grid.get_cell(segment.x, segment.y + 1)
            if segment.y + 1 < self.grid_height and (value == 10 or value == 11 or value == 12 or value == 20):
                return

        # 开始掉落
        self.is_falling = True

        for segment in [self.snake_head] + self.snake_body:
            self.set_cell(segment.x, segment.y, 0)
            segment.y += 1
            self.set_cell(segment.x, segment.y, 31 if segment == self.snake_head else 30)
