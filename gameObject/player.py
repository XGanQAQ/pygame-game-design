import pygame
from pygame.math import Vector2
from pygame import Surface

class Player(pygame.sprite.Sprite):  # 继承 Sprite 类
    def __init__(self, initial_pos: Vector2, image: Surface):
        super().__init__()  # 初始化 Sprite
        self.image = image if image else Surface((20, 20))  # 如果没有图像，创建一个默认的矩形
        if not image:
            self.image.fill((255, 0, 0))  # 默认图像填充为红色
        self.rect = self.image.get_rect(topleft=(initial_pos.x, initial_pos.y))  # 使用 rect 管理位置
        self.move_speed = 200  # 每秒移动的像素数

    def update(self, sender, delta_time):
        """
        更新玩家状态（如果需要）
        :param sender: 信号发送者
        :param delta_time: 时间增量（秒）
        """
        keys = pygame.key.get_pressed()
        direction = Vector2(0, 0)

        if keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_RIGHT]:
            direction.x += 1
        if keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_DOWN]:
            direction.y += 1

        if direction.length() > 0:
            direction.scale_to_length(1)
        self.move(direction, delta_time)

    def draw(self, sender, screen):
        """
        绘制玩家到屏幕上
        :param sender: 信号发送者
        :param screen: 游戏屏幕
        """
        screen.blit(self.image, self.rect.topleft)

    def move(self, direction: Vector2, delta_time):
        """
        根据方向和时间增量更新玩家位置
        :param direction: 方向向量 (Vector2)
        :param delta_time: 时间增量（秒）
        """
        displacement = direction * self.move_speed * delta_time
        self.rect.x += displacement.x
        self.rect.y += displacement.y

    def set_image(self, image):
        """
        设置玩家图像
        :param image: 图像对象
        """
        self.image = image
        self.rect = self.image.get_rect(topleft=self.rect.topleft)  # 更新 rect 大小


