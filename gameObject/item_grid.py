from gameObject.gridmap import Gridmap
import pygame

class ItemGrid(Gridmap):
    """
    物品层：存放物品的网格数据
    0 代表空白
    50 代表苹果
    51 代表浮空药水
    52 代表无敌星星
    53 代表加速药水
    """
    def __init__(self, width, height, cell_size=20):
        super().__init__(width, height)
        self.cell_size = cell_size  # 单元格大小
        self.art_assets = {} # 新增：用于存放美术资源信息
        self.item_effects_config = {
            51: {'duration': 5000},  # 浮空药水: 持续时间
            52: {'duration': 5000},  # 无敌星星: 持续时间
            53: {'duration': 5000, 'multiplier': 0.5}  # 加速药水: 持续时间, 速度倍率
        }

    def get_item_effect_config(self, item_id: int):
        """
        根据物品ID获取其效果配置
        :param item_id: 物品的ID
        :return: 包含效果参数的字典，如果物品ID没有配置则返回None
        """
        return self.item_effects_config.get(item_id)

    def draw(self, screen):
        """
        绘制物品层
        红色圆点表示苹果。
        青色圆点表示浮空药水。
        黄色圆点表示无敌星星。
        绿色圆点表示加速药水。
        """
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_value = self.get_cell(x, y)
                if cell_value == 50:  # 苹果
                    pygame.draw.circle(screen, (255, 0, 0), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                elif cell_value == 51:  # 浮空药水
                    pygame.draw.circle(screen, (0, 255, 255), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                elif cell_value == 52:  # 无敌星星
                    pygame.draw.circle(screen, (255, 255, 0), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                elif cell_value == 53:  # 加速药水
                    pygame.draw.circle(screen, (0, 255, 0), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 3)

    def roll(self):
        """
        滚动物品层
        """
        for y in range(self.grid_height - 1, 0, -1):
            for x in range(self.grid_width):
                self.set_cell(x, y, self.get_cell(x, y - 1))
        for x in range(self.grid_width):
            self.set_cell(x, 0, 0)

    def set_apple(self, x, y):
        """设置苹果"""
        self.set_cell(x, y, 50)

    def set_float_potion(self, x, y):
        """设置浮空药水"""
        self.set_cell(x, y, 51)

    def set_invincible_star(self, x, y):
        """设置无敌星星"""
        self.set_cell(x, y, 52)

    def set_speed_potion(self, x, y):
        """设置加速药水"""
        self.set_cell(x, y, 53)

    def is_apple(self, x, y):
        """检查是否是苹果"""
        return self.get_cell(x, y) == 50

    def is_float_potion(self, x, y):
        """检查是否是浮空药水"""
        return self.get_cell(x, y) == 51

    def is_invincible_star(self, x, y):
        """检查是否是无敌星星"""
        return self.get_cell(x, y) == 52

    def is_speed_potion(self, x, y):
        """检查是否是加速药水"""
        return self.get_cell(x, y) == 53
