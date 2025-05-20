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
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            self.width = int(lines[0].strip())  # 第一行是宽度
            self.height = int(lines[1].strip())  # 第二行是高度
            self.map_data = [
                list(map(int, line.split())) 
                for line in lines[2:] if line.strip()  # 跳过空行
            ]

    def get_map_data(self):
        """
        获取地图数据。
        """
        return self.map_data
