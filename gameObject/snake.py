from locale import windows_locale
from gameObject.int_vector2 import IntVector2
from collections import deque
from blinker import Signal
from enum import IntFlag
from enum import Enum
from gameObject.item_grid import ItemGrid

class MoveStatus(Enum):
    NONE = 0
    MOVE = 1
    FALL = 3

class CollisionStatus(IntFlag):
    NONE = 0
    DIE = 4 
    GROW = 8
    FLOAT = 16 #浮空
    INVINCIBLE = 32 #无敌
    SPEED_BOOST = 64 #加速
    GET_HURT = 128 #受伤 
    WIN = 256 #通关

class Snake():
    def __init__(self, snake_body: deque[IntVector2], item_grid: ItemGrid):
        self._snake_body = snake_body
        self.snake_move_status = MoveStatus.NONE
        self.snake_collision_status = CollisionStatus.NONE

        # Singnal
        self.snake_init_signal = Signal()  # 蛇初始化信号
        self.snak_dead_signal = Signal()  # 蛇死亡信号
        self.snake_grow_signal = Signal()  # 蛇生长信号
        self.snake_win_signal = Signal()  # 蛇通关信号

        # Move Speed
        self.move_speed = 500  # Speed of the snake movement
        self.move_speed_buffer = 0
        self.move_speed_buffer_max = 100  # Speed buffer to control the speed of the snake

        self.next_move_is_wall = False
        
        # Fall Speed
        self.is_enable_fall:bool = True
        self.fall_speed = 500  # 掉落速度
        self.fall_speed_buffer = 0
        self.fall_speed_buffer_max = 100  # 掉落速度缓冲区最大值
        
        # Float effect
        self.float_effect_timer = 0  # 浮空效果计时器

        # Invincible effect
        self.invincible_effect_timer = 0  # 无敌效果计时器

        # Speed boost effect
        self.speed_boost_effect_timer = 0  # 加速效果计时器
        self.original_move_speed = self.move_speed # 存储原始移动速度

        self.item_config = item_grid.item_effects_config

    @property
    def snake_head(self):
        return self._snake_body[0]
    
    @property
    def snake_body(self):
        return self._snake_body

    @property
    def snake_tail(self):
        return self._snake_body[-1]

    @property
    def snake_length(self):
        return len(self._snake_body)

    def update(self, delta_time, direction: IntVector2, snake_grid=None, plat_grid=None, item_grid=None, enemy_grid=None):
        self.__check_move_status(direction, snake_grid, plat_grid, item_grid, enemy_grid)
        self.__check_fall_status(plat_grid)
        self.__check_head_collision(plat_grid, item_grid, enemy_grid)
        self.__check_body_collision(plat_grid, item_grid, enemy_grid)
        self.__update_move(delta_time, direction)
        self.__update_fall(delta_time)

        # 更新浮空效果计时器
        if self.snake_collision_status & CollisionStatus.FLOAT:
            self.float_effect_timer -= delta_time * 1000  # delta_time 是秒，转换为毫秒
            if self.float_effect_timer <= 0:
                self.snake_collision_status &= ~CollisionStatus.FLOAT
                self.float_effect_timer = 0

        # 更新无敌效果计时器
        if self.snake_collision_status & CollisionStatus.INVINCIBLE:
            self.invincible_effect_timer -= delta_time * 1000  # delta_time 是秒，转换为毫秒
            if self.invincible_effect_timer <= 0:
                self.snake_collision_status &= ~CollisionStatus.INVINCIBLE
                self.invincible_effect_timer = 0

        # 更新加速效果计时器
        if self.snake_collision_status & CollisionStatus.SPEED_BOOST:
            self.speed_boost_effect_timer -= delta_time * 1000  # delta_time 是秒，转换为毫秒
            if self.speed_boost_effect_timer <= 0:
                self.snake_collision_status &= ~CollisionStatus.SPEED_BOOST
                self.move_speed = self.original_move_speed  # 恢复原始速度
                self.speed_boost_effect_timer = 0
    
    def __update_move(self, delta_time, direction: IntVector2):
        # Move speed buffer 移动计时器
        if self.move_speed_buffer < self.move_speed_buffer_max:
            self.move_speed_buffer += delta_time * self.move_speed
            return
        self.move_speed_buffer %= self.move_speed_buffer_max

        if self.next_move_is_wall:
            return

        # 如果未开启掉落，则默认移动
        if not self.is_enable_fall:
            self.snake_move_status = MoveStatus.MOVE
        
        # 如果有浮空效果，则默认移动
        if self.snake_collision_status & CollisionStatus.FLOAT:
            self.snake_move_status = MoveStatus.MOVE

        if self.snake_move_status == MoveStatus.MOVE and (CollisionStatus.GROW in self.snake_collision_status):
            self.__move_grow(direction)
            self.snake_collision_status &= ~CollisionStatus.GROW
            return
        elif self.snake_move_status == MoveStatus.MOVE:
            self.__move(direction)
            return
    
    def __update_fall(self, delta_time):
        # Fall speed buffer 掉落计时器
        if self.fall_speed_buffer < self.fall_speed_buffer_max:
            self.fall_speed_buffer += delta_time * self.fall_speed
            return
        self.fall_speed_buffer %= self.fall_speed_buffer_max

        # 如果未开启掉落，则跳过
        if not self.is_enable_fall:
            return

        # 如果有浮空效果，则跳过
        if self.snake_collision_status & CollisionStatus.FLOAT:
            return

        if self.snake_move_status == MoveStatus.FALL:
            self.__fall()

    def __check_move_status(self,direction: IntVector2 ,snake_grid=None ,plat_grid=None, item_grid=None, enemy_grid=None):
        next_move_pos = self.snake_head + direction
        self.next_move_is_wall = False

        # 如果没有平台网格，则报错
        if not plat_grid:
            raise ValueError("Platform grid is not initialized.")

        # Check boundaries
        if next_move_pos.x < 0 or next_move_pos.x >= plat_grid.grid_width or next_move_pos.y < 0 or next_move_pos.y >= plat_grid.grid_height:
            print("Cant move! Hit boundary.")
            self.next_move_is_wall = True
        
        # 检查蛇是否调出底下
        if next_move_pos.y >= plat_grid.grid_height:
            print("Game Over! Hit bottom.")
            self.snake_move_status = MoveStatus.NONE
            self.snak_dead_signal.send(self)
            return

        # Check self-collision
        if snake_grid.get_cell(next_move_pos.x, next_move_pos.y) == 30:
            print("Game Over! Self-collision.")
            self.next_move_is_wall = True

        # Check platform collision
        if plat_grid:
            value = plat_grid.get_cell(next_move_pos.x, next_move_pos.y)
            if value == 10: # Platform
                print("Cant move! Hit platform.")
                self.next_move_is_wall = True
            elif value == 11: # Platform
                print("Cant move! Hit platform.")
                self.next_move_is_wall = True

        if item_grid:
            value = item_grid.get_cell(next_move_pos.x, next_move_pos.y)
            if value == 50: # Apple
                print("Grow!")
                # item_grid.set_cell(next_move_pos.x, next_move_pos.y, 0)
                self.snake_collision_status |= CollisionStatus.GROW

        if enemy_grid:
            pass

        self.snake_move_status = MoveStatus.MOVE

    def __check_fall_status(self, plat_grid=None):
        # 如果没有平台网格，则报错
        if not plat_grid:
            raise ValueError("Platform grid is not initialized.")

        have_plat = False

        for segment in self.snake_body:
            value = plat_grid.get_cell(segment.x, segment.y + 1)
            if segment.y + 1 < plat_grid.grid_height and (value == 10 or value == 11 or value == 12):
                have_plat = True
        
        if not have_plat:
            self.snake_move_status = MoveStatus.FALL

    def __check_head_collision(self, plat_grid=None, item_grid=None, enemy_grid=None):
        head_pos = self.snake_head

        if plat_grid:
            pass

        if item_grid:
            value = item_grid.get_cell(head_pos.x, head_pos.y)

            if value == 50: # Apple
                item_grid.set_cell(head_pos.x, head_pos.y, 0)
                pass
            elif value == 51: # Float potion
                item_grid.set_cell(head_pos.x, head_pos.y, 0) # 移除药水
                self.float_effect_timer = self.item_config[51]['duration']
                self.snake_collision_status |= CollisionStatus.FLOAT
            elif value == 52: # Invincible star
                item_grid.set_cell(head_pos.x, head_pos.y, 0) # 移除星星
                self.invincible_effect_timer = self.item_config[52]['duration']
                self.snake_collision_status |= CollisionStatus.INVINCIBLE
            elif value == 53: # Speed boost potion
                item_grid.set_cell(head_pos.x, head_pos.y, 0) # 移除药水
                self.speed_boost_effect_timer = self.item_config[53]['duration']
                self.move_speed *= 1 + self.item_config[53]['multiplier']
                self.snake_collision_status |= CollisionStatus.SPEED_BOOST

        if enemy_grid:
            pass

    def __check_body_collision(self, plat_grid=None, item_grid=None, enemy_grid=None):
        body_pos = self.snake_body

        for pos in body_pos:
            if plat_grid:
                value = plat_grid.get_cell(pos.x, pos.y)
                if value == 20: # 尖刺
                    if not self.snake_collision_status & CollisionStatus.INVINCIBLE:
                        print("Game Over! Hit 尖刺.")
                        self.snake_collision_status |= CollisionStatus.DIE

            if item_grid:
                value = item_grid.get_cell(pos.x, pos.y)
                if value == 54: # 通关标志
                    print("Win!")
                    self.snake_win_signal.send(self)
                    item_grid.set_cell(pos.x, pos.y, 0)

            if enemy_grid:
                value = enemy_grid.get_cell(pos.x, pos.y)

                if value == 40:
                    if not self.snake_collision_status & CollisionStatus.INVINCIBLE:
                        print("Game Over! Hit enemy.")
                        self.snake_collision_status |= CollisionStatus.DIE

    def __move(self, direction: IntVector2):
        new_head = self.snake_head + direction
        self._snake_body.appendleft(new_head)
        self._snake_body.pop()

    def __move_grow(self, direction: IntVector2):
        new_head = self.snake_head + direction
        self._snake_body.appendleft(new_head)

    # 所有队列中的元素都向下移动一格
    def __fall(self):
        for i in range(len(self._snake_body)):
            self._snake_body[i] += IntVector2(0, 1)

    def roll(self):
        for i in range(len(self._snake_body)):
            self._snake_body[i] += IntVector2(0, 1)
        