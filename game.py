import pygame
from gameObject.player import Player
from pygame.math import Vector2
from gameObject.SpriteSheet import SpriteSheet
import tools
from typing import List, Dict, Optional, Union

class Game:
    def __init__(self, screen_size):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size) # 设置窗口大小
        pygame.display.set_caption("Game Window") # 设置窗口标题
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png")) # 设置窗口图标
        self.screen.fill("white") # 填充背景颜色

        self.clock = pygame.time.Clock()
        self.running = True

    def init_game_objects(self, player_pos):
        self.player = Player(player_pos, image=None)


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
        self.player.update(delta_time)

    def draw(self):
        # 清空屏幕
        self.screen.fill("white")

        # 绘制玩家
        self.player.draw(self.screen)

    def quit(self):
        pygame.quit()
