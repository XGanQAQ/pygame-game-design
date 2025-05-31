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
