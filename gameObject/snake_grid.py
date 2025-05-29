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
        self.snake_tail: Optional[IntVector2] = None  # 蛇尾位置

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
        self.snake_tail_image = None

        # Move and falling states
        self.is_enable_falling = False  # 是否允许掉落
        self.is_falling = False  # 是否正在掉落

        # Float effect
        self.float_effect_timer = 0  # 浮空效果计时器
        self.is_floating_effect_active = False # 浮空效果是否激活

        # Invincible effect
        self.invincible_effect_timer = 0  # 无敌效果计时器
        self.is_invincible_effect_active = False # 无敌效果是否激活

        # Speed boost effect
        self.speed_boost_effect_timer = 0  # 加速效果计时器
        self.is_speed_boost_active = False  # 加速效果是否激活
        self.original_move_speed = self.move_speed # 存储原始移动速度

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

        # 如果不处于掉落状态并且满足移动需求逻辑，则可以移动蛇
        if not self.is_falling and self.__move_speed_logic(delta_time):
            self.__move_snake(self.direction, plat_grid, item_grid, enemy_grid)

        # 如果允许掉落，则开启掉落
        if self.is_enable_falling:
            self.__fall(delta_time, plat_grid)

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
        
        # Then draw the tail with special color or image if it exists
        if self.snake_tail and self.get_cell(self.snake_tail.x, self.snake_tail.y) == 30:
            if hasattr(self, 'snake_tail_image') and self.snake_tail_image is not None:
                # 如果有设置蛇尾图片，则使用图片
                screen.blit(self.snake_tail_image, 
                          (self.snake_tail.x * self.cell_size, 
                           self.snake_tail.y * self.cell_size))
            else:
                # 否则使用默认的绿色矩形
                pygame.draw.rect(screen, (0, 150, 0), 
                              (self.snake_tail.x * self.cell_size, 
                               self.snake_tail.y * self.cell_size, 
                               self.cell_size, self.cell_size))

    def roll(self):
        """
        滚动蛇层
        先保存当前蛇的位置，然后清空整个网格，最后重新设置滚动后的位置
        """
        # 保存当前所有蛇身和头部的位置
        snake_cells = []
        head_at_bottom = False
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_value = self.get_cell(x, y)
                if cell_value in [30, 31]:  # 蛇身或蛇头
                    snake_cells.append((x, y, cell_value))
                    # 检查蛇头是否在最底层
                    if cell_value == 31 and y == self.grid_height - 1:
                        head_at_bottom = True
        
        # 如果蛇头在最底层，触发死亡信号
        if head_at_bottom:
            self.snak_dead_signal.send(self)
            return
        
        # 清空整个网格
        self.clear()
        
        # 重新设置滚动后的位置
        for x, y, cell_value in snake_cells:
            new_y = y + 1  # 向下滚动一格
            if new_y < self.grid_height:  # 如果新位置在网格内
                self.set_cell(x, new_y, cell_value)
                # 更新蛇头或蛇尾的引用
                if cell_value == 31:  # 蛇头
                    self.snake_head = IntVector2(x, new_y)
                elif (x, y) == (self.snake_tail.x, self.snake_tail.y):  # 蛇尾
                    self.snake_tail = IntVector2(x, new_y)
            
            # 更新蛇身列表中的位置
            for i, pos in enumerate(self.snake_body):
                if (pos.x, pos.y) == (x, y):
                    if new_y < self.grid_height:
                        self.snake_body[i] = IntVector2(x, new_y)
                    else:
                        # 如果蛇身移出网格，则从蛇身列表中移除
                        self.snake_body.pop(i)
                        if self.snake_body:  # 如果还有蛇身，更新蛇尾
                            self.snake_tail = IntVector2(self.snake_body[-1].x, self.snake_body[-1].y)
                        break

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
            item_config = item_grid.get_item_effect_config(value)

            if value == 50: # Apple
                self.__add_snake_body()
                item_grid.set_cell(new_head.x, new_head.y, 0)
            elif value == 51 and item_config: # Float potion
                self.is_enable_falling = False
                self.is_floating_effect_active = True
                self.float_effect_timer = item_config['duration']
                item_grid.set_cell(new_head.x, new_head.y, 0) # 移除药水
            elif value == 52 and item_config: # Invincible star
                self.is_invincible_effect_active = True
                self.invincible_effect_timer = item_config['duration']
                item_grid.set_cell(new_head.x, new_head.y, 0) # 移除星星
            elif value == 53 and item_config: # Speed boost potion
                if not self.is_speed_boost_active: # 只有在加速效果未激活时才保存原始速度
                    self.original_move_speed = self.move_speed
                self.is_speed_boost_active = True
                self.speed_boost_effect_timer = item_config['duration']
                self.move_speed = self.original_move_speed * (1 + item_config['multiplier'])
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
            # 更新蛇尾位置为新的最后一个身体部分
            self.snake_tail = self.snake_body[-1] if self.snake_body_length > 1 else self.snake_head
        else:
            # 如果没有身体，蛇尾就是蛇头
            self.snake_tail = self.snake_head

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
        # 更新蛇尾位置
        self.snake_tail = new_tail

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
            self.set_cell(segment.x, segment.y, 0)  # 擦除旧位置

        for segment in [self.snake_head] + self.snake_body:
            segment.y += 1  # 更新位置
            self.set_cell(segment.x, segment.y, 31 if segment == self.snake_head else 30)  # 绘制新位置
