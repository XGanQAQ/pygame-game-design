import pygame
from pygame.math import Vector2
from pygame import Surface

class NPC(pygame.sprite.Sprite):
    def __init__(self, initial_pos: Vector2, image: Surface):
        super().__init__()
        self.image = image if image else Surface((20, 20))
        if not image:
            self.image.fill((0, 255, 0))  # 默认图像填充为绿色
        self.rect = self.image.get_rect(topleft=(initial_pos.x, initial_pos.y))

    def update(self, sender, delta_time):
        """
        更新 NPC 状态（如果需要）
        :param sender: 信号发送者
        :param delta_time: 时间增量（秒）
        """
        # NPC 的逻辑可以在这里实现，例如自动移动或与玩家交互
        pass

    def interact(self, player):
        """
        与玩家交互
        :param player: 玩家对象
        """
        if self.rect.colliderect(player.rect):
            print("玩家与 NPC 发生了交互！")
