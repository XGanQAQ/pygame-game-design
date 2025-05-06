from gridmap import Gridmap
class GameMap:
    def __init__(self, width, height):
        self.plat_map = Gridmap(width, height)
        self.player_map = Gridmap(width, height)
        self.enemy_map = Gridmap(width, height)
        self.item_map = Gridmap(width, height)
    
    def roll(self):
        """
        滚动地图
        把所有地图的格子向下滚动一格
        """
        for y in range(self.plat_map.height-1, 0, -1):
            for x in range(self.plat_map.width):
                self.plat_map.set_cell(x, y, self.plat_map.get_cell(x, y-1))
                self.player_map.set_cell(x, y, self.player_map.get_cell(x, y-1))
                self.enemy_map.set_cell(x, y, self.enemy_map.get_cell(x, y-1))
                self.item_map.set_cell(x, y, self.item_map.get_cell(x, y-1))
        # 随机生成新的一行
        # 这里可以添加随机生成地图的逻辑
        for x in range(self.plat_map.width):
            self.plat_map.set_cell(x, 0, None)
            self.player_map.set_cell(x, 0, None)
            self.enemy_map.set_cell(x, 0, None)
            self.item_map.set_cell(x, 0, None)

    def check_collision(self, x, y):
        """
        检查玩家是否与地图上的物体发生碰撞
        :param x: 玩家在地图上的x坐标
        :param y: 玩家在地图上的y坐标
        :return: True表示发生碰撞，False表示没有发生碰撞
        """
        if self.plat_map.get_cell(x, y) is not None:
            return True
        return False