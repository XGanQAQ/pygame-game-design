import sys
import os
# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from pygame.math import Vector2
from gameObject.player import Player
from game import Game

def initialize_player(game):
    """
    初始化玩家对象并注册信号
    :param game: Game 实例
    """
    player_start_pos = Vector2(0, game.screen.get_height() - 20)  # 设置玩家初始位置
    player_image = pygame.image.load("assets/images/icon.png")  # 加载玩家图像
    player = Player(player_start_pos, player_image)  # 创建玩家对象

    # 将 player 存储在 game 实例中
    game.player = player

    # 注册更新和绘制信号
    game.signals["on_update"].connect(player.update)
    game.signals["on_draw"].connect(player.draw)

# 初始化游戏
game = Game((800, 600))  # 设置屏幕大小

# 注册初始化信号
game.signals["on_game_init"].connect(initialize_player)

# 初始化游戏对象
game.__init_game_objects()

# 运行游戏
game.run()
