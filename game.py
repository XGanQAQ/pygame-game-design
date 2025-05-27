from typing import List, Dict, Optional, Union
import pygame
from pygame.math import Vector2
from blinker import Signal  # 引入 blinker 信号库

from gameObject.player import Player
from gameObject.snake_grid import SnakeGrid
from gameObject.sprite_sheet import SpriteSheet
from gameObject.gridmap import Gridmap

from enum import Enum

import tools


class LifeCycle(Enum):
    INIT = "init"  # 初始化
    UPDATE = "update"  # 更新
    DRAW = "draw"  # 绘制
    QUIT = "quit"  # 退出
    GAME_OVER = "game_over"  # 游戏结束
    GAME_START = "game_start"  # 游戏开始
    GAME_PAUSE = "game_pause"  # 游戏暂停

class Game:
    _instance = None  # 用于存储单例实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, screen_size):
        if not hasattr(self, "initialized"):  # 防止重复初始化
            pygame.init()
            self.screen = pygame.display.set_mode(screen_size)  # 设置窗口大小
            pygame.display.set_caption("Game Window")  # 设置窗口标题
            pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))  # 设置窗口图标
            self.screen.fill("white")  # 填充背景颜色

            self.clock = pygame.time.Clock()
            self.running = True

            # 初始化信号
            self.signals = {
                LifeCycle.INIT: Signal(),  # 初始化时触发
                LifeCycle.UPDATE: Signal(),  # 每帧更新时触发
                LifeCycle.DRAW: Signal(),    # 每帧绘制时触发
                LifeCycle.QUIT: Signal()     # 退出时触发
            }
            
            self.initialized = True  # 标记已初始化

    def init_game_objects(self):
        self.signals[LifeCycle.INIT].send(self)  # 触发初始化信号

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # 获取时间增量（秒）
            self.update(delta_time)
            self.draw()
            pygame.display.flip()  # 更新整个屏幕的显示内容
            self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击×关闭窗口
                self.running = False
                self.signals[LifeCycle.QUIT].send(self)  # 触发退出信号
                self.quit()
                return  # 确保退出后不再继续执行

    def update(self, delta_time):
        # 触发更新信号
        self.signals[LifeCycle.UPDATE].send(self, delta_time=delta_time)

    def draw(self):
        # 清空屏幕
        self.screen.fill("white")

        # 触发绘制信号
        self.signals[LifeCycle.DRAW].send(self, screen=self.screen)

    def quit(self):
        pygame.quit()
        self.running = False  # 确保主循环不会继续运行
