from gameObject.gridmap import Gridmap
import pygame
import random

class EnemyGrid(Gridmap):
    """
    敌人层：存放敌人的网格数据
    0 代表空白
    40 代表巡逻敌人
    41 代表飞行敌人
    42 代表追踪敌人
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        self.cell_size = 20  # 单元格大小

    def update(self, player_pos):
        """
        更新敌人状态，例如巡逻敌人移动、飞行敌人随机移动、追踪敌人追踪玩家
        :param player_pos: 玩家位置 (x, y)
        """
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_value = self.get_cell(x, y)
                if cell_value == 40:  # 巡逻敌人
                    if x + 1 < self.grid_width and self.get_cell(x + 1, y) == 0:
                        self.set_cell(x + 1, y, 40)
                        self.set_cell(x, y, 0)
                elif cell_value == 41:  # 飞行敌人
                    dx, dy = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height and self.get_cell(nx, ny) == 0:
                        self.set_cell(nx, ny, 41)
                        self.set_cell(x, y, 0)
                elif cell_value == 42:  # 追踪敌人
                    dx = 1 if player_pos[0] > x else -1 if player_pos[0] < x else 0
                    dy = 1 if player_pos[1] > y else -1 if player_pos[1] < y else 0
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height and self.get_cell(nx, ny) == 0:
                        self.set_cell(nx, ny, 42)
                        self.set_cell(x, y, 0)

    def draw(self, screen):
        """
        绘制敌人层
        红色矩形表示巡逻敌人（会左右移动）。
        蓝色圆点表示飞行敌人（会随机移动）。
        黄色矩形表示追踪敌人（会追踪玩家位置）。
        """
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_value = self.get_cell(x, y)
                if cell_value == 40:  # 巡逻敌人
                    pygame.draw.rect(screen, (255, 0, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif cell_value == 41:  # 飞行敌人
                    pygame.draw.circle(screen, (0, 0, 255), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                elif cell_value == 42:  # 追踪敌人
                    pygame.draw.rect(screen, (255, 255, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
    def roll(self):
        """
        滚动敌人层
        """
        for y in range(self.grid_height - 1, 0, -1):
            for x in range(self.grid_width):
                self.set_cell(x, y, self.get_cell(x, y - 1))
        for x in range(self.grid_width):
            self.set_cell(x, 0, 0)

    def set_patrol_enemy(self, x, y):
        """设置巡逻敌人"""
        self.set_cell(x, y, 40)

    def set_flying_enemy(self, x, y):
        """设置飞行敌人"""
        self.set_cell(x, y, 41)

    def set_tracking_enemy(self, x, y):
        """设置追踪敌人"""
        self.set_cell(x, y, 42)
