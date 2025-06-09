from typing import List, Dict, Optional, Union
from blinker import Signal  # 引入 blinker 信号库
import pygame
import pygame_gui
from pygame.math import Vector2


from gameObject.player import Player
from gameObject.snake_grid import SnakeGrid
from gameObject.sprite_sheet import SpriteSheet
from gameObject.gridmap import Gridmap
from gameObject.game_object import GameObject

from enum import Enum

import tools


class LifeCycle(Enum):
    INIT = "init"  # 初始化
    UPDATE = "update"  # 更新
    EVENT = "event"  # 事件
    DRAW = "draw"  # 绘制
    QUIT = "quit"  # 退出
    GAME_OVER = "game_over"  # 游戏结束
    GAME_START = "game_start"  # 游戏开始
    GAME_PAUSE = "game_pause"  # 游戏暂停
    GAME_RESUME = "game_resume"  # 游戏恢复

class Game:
    _instance = None  # 用于存储单例实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def set_window_icon(self, icon_path: str = "assets/images/icon.png"):
        """
        设置窗口图标
        :param icon_path: 图标文件路径
        """
        try:
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
            return True
        except pygame.error as e:
            print(f"无法加载图标文件 {icon_path}: {e}")
            return False

    def __init__(self, screen_size: Union[tuple, Vector2] = (1600, 900)):
        if not hasattr(self, "initialized"):  # 防止重复初始化
            pygame.init()
            self.screen = pygame.display.set_mode(screen_size)  # 设置窗口大小
            pygame.display.set_caption("Game Window")  # 设置窗口标题
            self.set_window_icon()  # 设置窗口图标
            self.screen.fill("black")  # 填充背景颜色

            # 背景图属性
            self.background = None
            self.background_rect = None

            self.clock = pygame.time.Clock()
            self.running = True

            # 初始化信号
            self.signals = {
                LifeCycle.INIT: Signal(),  # 初始化时触发
                LifeCycle.UPDATE: Signal(),  # 每帧更新时触发
                LifeCycle.EVENT: Signal(),  # 事件时触发
                LifeCycle.DRAW: Signal(),    # 每帧绘制时触发
                LifeCycle.QUIT: Signal(),     # 退出时触发
                LifeCycle.GAME_START: Signal(),  # 游戏开始时触发
                LifeCycle.GAME_OVER: Signal(),  # 游戏结束时触发
                LifeCycle.GAME_PAUSE: Signal(),  # 游戏暂停时触发
                LifeCycle.GAME_RESUME: Signal(),  # 游戏恢复时触发
            }
            
            self.initialized = True  # 标记已初始化】

    def init_game_objects(self):
        self.signals[LifeCycle.INIT].send(self, screen=self.screen)  # 触发初始化信号

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # 获取时间增量（秒）
            self.__update(delta_time)
            self.__draw()
            self.__handle_events()

    def addGameObject(self, game_object):
        """
        添加游戏对象，将其信号添加到游戏循环中。
        """
        if isinstance(game_object, GameObject):
            self.signals[LifeCycle.INIT].connect(game_object.init)  # 连接初始化信号
            self.signals[LifeCycle.UPDATE].connect(game_object.update)
            self.signals[LifeCycle.EVENT].connect(game_object.event)
            self.signals[LifeCycle.DRAW].connect(game_object.draw)
        else:
            raise TypeError("The game_object must be an instance of GameObject.")

    def load_background(self, image_path: str):
        """
        加载游戏背景图
        :param image_path: 背景图片的路径
        """
        try:
            self.background = pygame.image.load(image_path).convert()
            # 缩放背景图以匹配屏幕大小
            self.background = pygame.transform.scale(self.background, self.screen.get_size())
            self.background_rect = self.background.get_rect()
            return True
        except pygame.error as e:
            print(f"无法加载背景图片 {image_path}: {e}")
            self.background = None
            self.background_rect = None
            return False

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击×关闭窗口
                self.running = False
                self.signals[LifeCycle.QUIT].send(self)  # 触发退出信号
                self.quit()
                return  # 确保退出后不再继续执行
            self.signals[LifeCycle.EVENT].send(self, event=event)   # 触发事件信号
            

    def __update(self, delta_time):
        # 获取键盘输入状态
        keys = pygame.key.get_pressed()

        # 触发更新信号，并传递键盘输入状态和时间增量
        self.signals[LifeCycle.UPDATE].send(self, delta_time=delta_time, keys=keys)

    def __draw(self):
        # 清空屏幕
        self.screen.fill("black")
        
        # 绘制背景图（如果已加载）
        if self.background:
            self.screen.blit(self.background, self.background_rect)

        # 触发绘制信号，并传递屏幕对象
        self.signals[LifeCycle.DRAW].send(self, screen=self.screen)

        pygame.display.flip()

    def quit(self):
        pygame.quit()
        self.running = False  # 确保主循环不会继续运行
