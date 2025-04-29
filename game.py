from typing import List, Dict, Optional, Union
import pygame
from pygame.math import Vector2

from gameObject.player import Player
from gameObject.snake_grid import SnakeGrid
from gameObject.sprite_sheet import SpriteSheet
from gameObject.gridmap import Gridmap

import tools

class Game:
    def __init__(self, screen_size):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size) # 设置窗口大小
        pygame.display.set_caption("Game Window") # 设置窗口标题
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png")) # 设置窗口图标
        self.screen.fill("white") # 填充背景颜色

        self.clock = pygame.time.Clock()
        self.running = True

    def init_game_objects(self, player_pos:Vector2):
        self.snake_grid = SnakeGrid(20, 20) # 创建一个20x20的网格

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # 获取时间增量（秒）
            self.handle_events()
            self.update(delta_time)
            self.draw()
            pygame.display.flip() #​更新整个屏幕的显示内容

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #点击×关闭窗口
                self.running = False
                self.quit()

    def update(self, delta_time):
        # 更新玩家位置
        self.snake_grid.update()

    def draw(self):
        # 清空屏幕
        self.screen.fill("white")

        # 绘制网格
        self.snake_grid.draw(self.screen)

    def quit(self):
        pygame.quit()
