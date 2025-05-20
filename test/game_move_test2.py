import pygame
import sys
import os
# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pygame.math import Vector2
from gameObject.player import Player
from gameObject.npc import NPC

pygame.init()

# 初始化屏幕
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 创建玩家和 NPC
player = Player(Vector2(100, 100), None)
npc = NPC(Vector2(400, 300), None)

# 精灵组
all_sprites = pygame.sprite.Group(player, npc)

running = True
while running:
    delta_time = clock.tick(60) / 1000  # 帧时间（秒）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新精灵
    all_sprites.update(None, delta_time)

    # 检测玩家与 NPC 的交互
    npc.interact(player)

    # 绘制
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()