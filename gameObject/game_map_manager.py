from gameObject.gridmap import Gridmap
from gameObject.plat_grid import PlatGrid
from gameObject.snake_grid import SnakeGrid
from gameObject.enemy_grid import EnemyGrid
from gameObject.item_grid import ItemGrid
from gameObject.level_loader import LevelLoader

class GameMapManager:
    """
    统筹管理所有层级的地图，包括平台层、玩家层、敌人层、物品层。
    """
    def __init__(self, cell_size=20):
        self.cell_size = cell_size  # 单元格大小

        self.width = 0
        self.height = 0
        self.plat_grid = None  # 平台层
        self.snake_grid = None  # 玩家层
        self.enemy_grid = None  # 敌人层
        self.item_grid = None  # 物品层

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

    def load_level(self, file_path):
        """
        加载关卡文件并初始化地图。
        """
        level_loader = LevelLoader(file_path)
        level_loader.load_level()
        map_data = level_loader.get_map_data()

        self.width = level_loader.width
        self.height = level_loader.height
        self.plat_grid = PlatGrid(self.width, self.height, cell_size=self.cell_size)
        self.snake_grid = SnakeGrid(self.width, self.height, cell_size=self.cell_size)
        self.enemy_grid = EnemyGrid(self.width, self.height, cell_size=self.cell_size)
        self.item_grid = ItemGrid(self.width, self.height, cell_size=self.cell_size)


        # 根据地图数据初始化各层
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                if cell == 10:  # 不可穿透的地面
                    self.plat_grid.set_cell(x, y, 10)
                elif cell == 50:  # 苹果
                    self.item_grid.set_cell(x, y, 50)
                # 其他物体可以在此扩展