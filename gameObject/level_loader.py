import csv

class LevelLoader:
    """
    关卡文件读取类，用于加载关卡地图。
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.width = 0
        self.height = 0
        self.map_data = []

    def load_level(self):
        """
        从文件中加载关卡数据。
        """
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

            self.width = int(rows[0][0])   # 第一行第一列是宽度
            self.height = int(rows[1][0])  # 第二行第一列是高度

            self.map_data = [
                list(map(int, row)) 
                for row in rows[2:] if row  # 跳过空行
            ]
        # TODO: 支持区分关卡内的小关卡

    def get_map_data(self):
        """
        获取地图数据。
        """
        return self.map_data
    
    def get_map_data_reverse(self):
        """
        获取地图数据的逆序。
        """
        return self.map_data[::-1]

    @staticmethod
    def filter_row_plat(row):
        """
        过滤出平台层的数据。
        """
        return [cell if cell in [10, 11, 20] else 0 for cell in row]

    @staticmethod
    def filter_row_snake(row):
        """
        过滤出蛇层的数据。
        """
        return [cell if cell in [30, 31, 32] else 0 for cell in row]

    @staticmethod
    def filter_row_enemy(row):
        """
        过滤出敌人层的数据。
        """
        return [cell if cell in [40, 41, 42] else 0 for cell in row]

    @staticmethod
    def filter_row_item(row):
        """
        过滤出物品层的数据。
        """
        return [cell if cell in [50, 51, 52, 53, 54] else 0 for cell in row]

