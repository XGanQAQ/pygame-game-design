import pygame
from pygame.math import Vector2
from pygame import Surface
# 参考游戏对象模板
class Player:
    def __init__(self, initial_pos:Vector2, image:Surface):
        self.player_pos = Vector2(initial_pos)  # 使用 Vector2 存储位置
        self.move_speed = 200  # 每秒移动的像素数
        self.image = image

    def update(self, delta_time):
        """
        更新玩家状态（如果需要）
        :param delta_time: 时间增量（秒）
        """
        # 玩家移动更新
        # 定义方向向量
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
        # 归一化方向向量，避免斜向移动速度更快
        if direction.length() > 0:
            direction.scale_to_length(1)
        self.move(direction, delta_time)  # 更新位置

        pass

    def draw(self, screen:Surface):
        """
        绘制玩家图像（如果有）
        :param screen: Pygame Surface 对象
        """
        if self.image:
            # 绘制玩家图像
            screen.blit(self.image, self.get_pos())
        else:
            # 如果没有图像，则绘制一个简单的圆点表示玩家
            pygame.draw.circle(screen, (255, 0, 0), (int(self.player_pos.x), int(self.player_pos.y)), 10)  # 红色圆点
    

    def move(self, direction:Vector2, delta_time):
        """
        根据方向和时间增量更新玩家位置
        :param direction: 方向向量 (Vector2)
        :param delta_time: 时间增量（秒）
        """
        self.player_pos += direction * self.move_speed * delta_time

    def get_pos(self)->Vector2:
        """
        获取玩家位置（转换为元组以便使用 Pygame 的绘制函数）
        :return: 元组 (x, y)
        """
        return tuple(self.player_pos)
    
    def set_image(self, image):
        """
        设置玩家图像
        :param image: 图像对象
        """
        self.image = image
