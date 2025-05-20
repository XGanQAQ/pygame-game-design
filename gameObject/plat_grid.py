from gameObject.gridmap import Gridmap
import random
import pygame

class PlatGrid(Gridmap):
    """
    平台层：存放平台的网格数据
    0 代表空白
    10 代表不可穿透的地面
        - 11 代表普通平台
        - 12 代表移动平台
    20 代表尖刺
    """
    def __init__(self, width, height, cell_size=20):
        super().__init__(width, height)
        self.cell_size = cell_size  # 单元格大小

    def update(self):
        """
        更新平台状态，例如移动平台的逻辑
        """
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.get_cell(x, y) == 12:  # 移动平台
                    # 示例逻辑：移动平台左右移动
                    if x + 1 < self.grid_width and self.get_cell(x + 1, y) == 0:
                        self.set_cell(x + 1, y, 12)
                        self.set_cell(x, y, 0)

    def draw(self, screen):
        """
        绘制平台层

        """
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_value = self.get_cell(x, y)
                if cell_value == 10:  # 不可穿透的地面
                    pygame.draw.rect(screen, (139, 69, 19), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif cell_value == 11:  # 普通平台
                    pygame.draw.rect(screen, (211, 211, 211), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif cell_value == 12:  # 移动平台
                    pygame.draw.rect(screen, (0, 200, 200), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif cell_value == 20:  # 尖刺
                    pygame.draw.polygon(screen, (255, 0, 0), [
                        (x * self.cell_size, (y + 1) * self.cell_size),
                        ((x + 0.5) * self.cell_size, y * self.cell_size),
                        ((x + 1) * self.cell_size, (y + 1) * self.cell_size)
                    ])

    def roll(self):
        """
        滚动平台层
        """
        # 将每一行向下移动一格
        for y in range(self.grid_height - 1, 0, -1):
            for x in range(self.grid_width):
                self.set_cell(x, y, self.get_cell(x, y - 1))

        # 生成新的一行
        for x in range(self.grid_width):
            self.set_cell(x, 0, 0)
            #新生成的行有可能是地面元素，也有可能是空白元素

            #为新生成的行添加地刺元素


    def set_ground(self, x, y):
        """设置不可穿透的地面"""
        self.set_cell(x, y, 10)

    def set_platform(self, x, y):
        """设置普通平台"""
        self.set_cell(x, y, 11)

    def set_moving_platform(self, x, y):
        """设置移动平台"""
        self.set_cell(x, y, 12)

    def set_spike(self, x, y):
        """设置尖刺"""
        self.set_cell(x, y, 20)

    def is_ground(self, x, y):
        """检查是否是不可穿透的地面"""
        return self.get_cell(x, y) == 10

    def is_platform(self, x, y):
        """检查是否是普通平台"""
        return self.get_cell(x, y) == 11

    def is_moving_platform(self, x, y):
        """检查是否是移动平台"""
        return self.get_cell(x, y) == 12

    def is_spike(self, x, y):
        """检查是否是尖刺"""
        return self.get_cell(x, y) == 20

