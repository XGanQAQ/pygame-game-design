import pygame
import gameObject
from game import Game

if __name__ == "__main__":
    # 创建游戏实例
    game = Game((800.0, 600.0))  # 屏幕大小和玩家初始位置

    try:
        game.init_game_objects((400.0, 300.0))  # 初始化游戏对象，传入玩家初始位置
        game.run()  # 运行游戏
    finally:
        game.quit()  # 确保退出时清理资源