from gameObject.gridmap import Gridmap
from gameObject.plat_grid import PlatGrid
from gameObject.snake_grid import SnakeGrid
from gameObject.enemy_grid import EnemyGrid
from gameObject.item_grid import ItemGrid

class GameMapManager:
    """
    统筹管理所有层级的地图，包括平台层、玩家层、敌人层、物品层。
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.plat_grid = PlatGrid(width, height)
        self.snake_grid = SnakeGrid(width, height)
        self.enemy_grid = EnemyGrid(width, height)
        self.item_grid = ItemGrid(width, height)

        self.is_rolling = False # 是否正在滚动
        self.roll_total = 0 # 滚动总计数器
        self.roll_count = 0 # 滚动计数器
        self.roll_speed = 10  # 滚动速度，每多少次update滚动一次，所以数值越大越慢

    def update(self, keys):
        """
        更新所有层级的地图状态。
        """
        self.snake_grid.update(keys,plat_grid=self.plat_grid ,item_grid=self.item_grid, enemy_grid=self.enemy_grid)
        self.enemy_grid.update(player_pos=(self.snake_grid.snake_head.x, self.snake_grid.snake_head.y))
        self.plat_grid.update()

        self.roll()  # 更新滚动状态

    def draw(self, screen):
        """
        绘制所有层级的地图。
        """
        self.plat_grid.draw(screen)
        self.item_grid.draw(screen)
        self.enemy_grid.draw(screen)
        self.snake_grid.draw(screen)

    def roll(self):
        """
        滚动所有层级的地图。
        """
        if self.is_rolling==False:
            return

        # 更新滚动逻辑
        self.roll_count += 1
        # 每roll_speed次update滚动一次
        if self.roll_count >= self.roll_speed:
            self.plat_grid.roll()
            # 玩家层不滚动,因为玩家受fall控制，而不是滚动影响
            self.enemy_grid.roll()
            self.item_grid.roll()
            self.roll_count = 0
            self.roll_total += 1

    def roll_grid(self, grid:Gridmap):
        """
        使网格的所有元素向下移动一格。
        最底部的一行将被清空，顶部新增一行空白。
        """
        for y in range(self.height - 1, 0, -1):
            for x in range(self.width):
                grid.set_cell(x, y, grid.get_cell(x, y - 1))
        for x in range(self.width):
            grid.set_cell(x, 0, 0)

    def set_snake_is_enable_falling(self, is_enable_falling:bool):
        """
        设置蛇是否允许掉落。
        """
        self.snake_grid.is_enable_falling = is_enable_falling