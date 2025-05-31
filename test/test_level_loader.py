import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from gameObject.level_loader import LevelLoader

class TestLevelLoader(unittest.TestCase):
    def setUp(self):
        # 创建一个临时关卡文件内容
        self.test_file_path = "test_level.csv"
        with open(self.test_file_path, "w") as file:
            file.write("5\n")  # 宽度
            file.write("5\n")  # 高度
            file.write("0,10,0,0,0\n")
            file.write("0,0,50,0,0\n")
            file.write("10,10,10,10,10\n")
            file.write("0,0,0,0,0\n")
            file.write("0,0,0,0,0\n")

    def tearDown(self):
        # 删除临时文件
        import os
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_load_level(self):
        # 测试LevelLoader是否正确加载关卡
        loader = LevelLoader(self.test_file_path)
        loader.load_level()

        self.assertEqual(loader.width, 5)
        self.assertEqual(loader.height, 5)
        self.assertEqual(loader.map_data, [
            [0, 10, 0, 0, 0],
            [0, 0, 50, 0, 0],
            [10, 10, 10, 10, 10],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])

if __name__ == "__main__":
    unittest.main()
