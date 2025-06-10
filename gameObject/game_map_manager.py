from gameObject.gridmap import Gridmap
from gameObject.plat_grid import PlatGrid
from gameObject.snake_grid import SnakeGrid
from gameObject.enemy_grid import EnemyGrid
from gameObject.item_grid import ItemGrid
from gameObject.level_loader import LevelLoader
from gameObject.game_object import GameObject
import pygame
from game import Game

class GameMapManager(GameObject):
    """
    统筹管理所有层级的地图，包括平台层、玩家层、敌人层、物品层。
    """
    def __init__(self, cell_size=20, map_background:pygame.Surface=None, screen_size:tuple=None):
        super().__init__()
        self.cell_size = cell_size  # 单元格大小

        self.map_data = [] # 读取的关卡数据
        self.width = 0
        self.height = 0
        self.plat_grid = None  # 平台层
        self.snake_grid = None  # 玩家层
        self.enemy_grid = None  # 敌人层
        self.item_grid = None  # 物品层

        self.map_screen = None # 地图屏幕
        self.map_background = map_background # 地图背景

        self.screen_size = screen_size # 屏幕大小

        self.is_rolling = False  # 是否正在滚动
        self.roll_total = 0  # 滚动总计数器
        self.roll_progress = 0.0  # 滚动进度(0.0-1.0)
        self.roll_speed = 1.0  # 滚动速度(格/秒)

        # 游戏状态
        self.is_game_start = False
        self.is_game_pause = False

        # level state
        self.level_path = "level/level_first_36x396.csv"
        self.level_read_row_count = 20

    def set_game_start(self, sender):
        self.is_game_start = True

    def init(self, sender, **kwargs):
        super().init(sender, **kwargs)

    def update(self, sender, **kwargs):
        """
        更新所有层级的地图状态。
        """
        if not self.is_game_start:
            return
        if self.is_game_pause:
            return
        keys = kwargs.get("keys", None)
        delta_time = kwargs.get("delta_time", 0)
        self.snake_grid.update(keys, delta_time, plat_grid=self.plat_grid, item_grid=self.item_grid, enemy_grid=self.enemy_grid)
        self.enemy_grid.update(player_pos=(self.snake_grid.snake.snake_head.x, self.snake_grid.snake.snake_head.y))
        self.plat_grid.update()
        self.roll(delta_time)  # 更新滚动状态，传入delta_time

        self.check_snake_out_screen()

    def event(self, sender, **kwargs):
        """
        处理所有层级的地图事件。
        """
        pass
    
    def draw(self, sender, **kwargs):
        """
        绘制所有层级的地图。
        """
        screen = kwargs.get("screen", None)
        
        if self.map_screen and screen:
            if self.map_background:
                self.map_screen.blit(self.map_background, (0, 0))
            else:
                self.map_screen.fill("black")
            self.item_grid.draw(self.map_screen)
            self.plat_grid.draw(self.map_screen)
            self.enemy_grid.draw(self.map_screen)
            self.snake_grid.draw(self.map_screen)
            screen.blit(self.map_screen, (350, 0)) # 将地图绘制到屏幕的(350, 0)位置 ，根据设计需求
            return
        
        if screen:
            self.plat_grid.draw(screen)
            self.item_grid.draw(screen)
            self.enemy_grid.draw(screen)
            self.snake_grid.draw(screen)
            return
        

    def roll(self, delta_time=0.0):
        """
        滚动所有层级的地图。
        
        Args:
            delta_time: 距离上一次更新的时间(秒)
        """
        if not self.is_rolling or delta_time <= 0:
            return
            
        # 更新滚动进度
        self.roll_progress += self.roll_speed * delta_time
        
        # 当进度达到或超过1.0时，执行滚动
        while self.roll_progress >= 1.0:
            new_row = self.map_data.pop(0) if self.map_data else [0] * self.width
            self.__perform_roll(new_row)
            self.roll_progress -= 1.0
    
    def __perform_roll(self, new_row=None):
        """执行一次完整的滚动操作"""
        plat_row = LevelLoader.filter_row_plat(new_row)
        snake_row = LevelLoader.filter_row_snake(new_row)
        enemy_row = LevelLoader.filter_row_enemy(new_row)
        item_row = LevelLoader.filter_row_item(new_row)
        
        self.plat_grid.push(plat_row)
        self.item_grid.push(item_row)
        self.snake_grid.roll()
        self.enemy_grid.push(enemy_row)
        self.roll_total += 1

    def set_snake_is_enable_falling(self, is_enable_falling:bool):
        """
        设置蛇是否允许掉落。
        """
        self.snake_grid.set_snake_is_enable_falling(is_enable_falling)
        
    def set_map_scrolling(self, enable: bool):
        """
        设置是否启用地图滚动。
        
        Args:
            enable (bool): 是否启用地图滚动
        """
        self.is_rolling = enable

    def load_level(self, file_path, read_row_count):
        """
        加载关卡文件并初始化地图。
        Args:
            file_path (str): 关卡文件路径
            read_row_count (int): 读取的行数，用于初始化地图
        """
        self.level_path = file_path
        self.level_read_row_count = read_row_count

        level_loader = LevelLoader(self.level_path)
        level_loader.load_level()
        self.map_data = level_loader.get_map_data_reverse()

        self.width = level_loader.width
        self.height = level_loader.height
        self.map_screen = pygame.Surface((self.cell_size * self.width, self.cell_size * self.height))
        self.plat_grid = PlatGrid(self.width, self.height, cell_size=self.cell_size)
        self.snake_grid = SnakeGrid(self.width, self.height, cell_size=self.cell_size)
        self.enemy_grid = EnemyGrid(self.width, self.height, cell_size=self.cell_size)
        self.item_grid = ItemGrid(self.width, self.height, cell_size=self.cell_size)
        
        # 推入指定行数的数据
        for _ in range(self.level_read_row_count):
            if not self.map_data:
                break
                
            row = self.map_data.pop(0)
            
            plat_row = LevelLoader.filter_row_plat(row)
            snake_row = LevelLoader.filter_row_snake(row)
            enemy_row = LevelLoader.filter_row_enemy(row)
            item_row = LevelLoader.filter_row_item(row)

            self.plat_grid.push(plat_row)
            self.snake_grid.push(snake_row)
            self.enemy_grid.push(enemy_row)
            self.item_grid.push(item_row)

        self.snake_grid.init_snake(self.item_grid)

    def on_game_start(self, sender):
        self.is_game_start = True
        self.is_game_pause = False

    def on_game_pause(self, sender):
        self.is_game_pause = True

    def on_game_over(self, sender):
        self.is_game_start = False
        self.is_game_pause = True

    def on_game_resume(self, sender):
        self.is_game_start = False
        self.is_game_pause = False

        # 重新加载关卡
        self.load_level(self.level_path, self.level_read_row_count)
        self.roll_total = 0

    def check_snake_out_screen(self):
        if self.snake_grid.snake.snake_head.y > self.screen_size[1]/self.cell_size:
            Game._instance.game_over(self)
            

        
        

        