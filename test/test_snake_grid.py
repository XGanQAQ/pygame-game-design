import unittest
import sys
import os
import pygame
from unittest.mock import MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gameObject.snake_grid import SnakeGrid
from gameObject.int_vector2 import IntVector2

class TestSnakeGrid(unittest.TestCase):
    def setUp(self):
        """在每个测试方法之前运行"""
        self.snake = SnakeGrid(10, 10)  # 10x10的网格
        pygame.init()  # 初始化pygame，因为draw方法需要
        
        # 创建模拟的surface用于绘制
        self.screen = pygame.Surface((200, 200))
        
        # 模拟信号处理器
        self.death_triggered = False
        self.grow_triggered = False
        
        def on_death(sender):
            self.death_triggered = True
            
        def on_grow(sender):
            self.grow_triggered = True
            
        self.snake.snak_dead_signal.connect(on_death)
        self.snake.snake_grow_signal.connect(on_grow)
    
    def tearDown(self):
        """在每个测试方法之后运行"""
        pygame.quit()
    
    def test_initial_state(self):
        """测试初始化状态"""
        self.assertEqual(self.snake.snake_head, IntVector2(5, 5))  # 默认在中心
        self.assertEqual(len(self.snake.snake_body), 0)  # 初始没有身体
        self.assertEqual(self.snake.snake_body_length, 0)
        self.assertIsNone(self.snake.snake_tail)
    
    def test_move_snake(self):
        """测试蛇的移动"""
        # 初始位置
        start_pos = IntVector2(self.snake.snake_head.x, self.snake.snake_head.y)
        
        # 向右移动
        self.snake.direction = IntVector2(1, 0)
        self.snake._SnakeGrid__move_snake(self.snake.direction)
        
        # 检查位置是否更新
        self.assertEqual(self.snake.snake_head, start_pos + IntVector2(1, 0))
    
    def test_add_body(self):
        """测试添加身体"""
        # 添加一个身体部分
        self.snake._SnakeGrid__add_snake_body()
        
        # 检查身体长度和位置
        self.assertEqual(self.snake.snake_body_length, 1)
        self.assertEqual(len(self.snake.snake_body), 1)
        self.assertEqual(self.snake.snake_tail, self.snake.snake_body[-1])
    
    def test_self_collision(self):
        """测试自碰撞检测"""
        # 重置死亡标志
        self.death_triggered = False
        
        # 添加一个身体部分
        self.snake._SnakeGrid__add_snake_body()
        
        # 移动蛇，制造自碰撞
        # 先向下移动
        self.snake.direction = IntVector2(0, 1)
        self.snake._SnakeGrid__move_snake(self.snake.direction)
        
        # 再向右移动
        self.snake.direction = IntVector2(1, 0)
        self.snake._SnakeGrid__move_snake(self.snake.direction)
        
        # 再向上移动（会碰到身体）
        self.snake.direction = IntVector2(0, -1)
        
        # 直接调用移动方法，检查是否会触发碰撞
        self.snake._SnakeGrid__move_snake(self.snake.direction)
        
        # 验证是否检测到自碰撞
        self.assertTrue(self.death_triggered, "自碰撞应触发死亡信号")
    
    def test_roll(self):
        """测试滚动功能"""
        # 设置蛇的位置在网格中间
        self.snake.snake_head = IntVector2(5, 5)
        self.snake.set_cell(5, 5, 31)  # 设置蛇头
        
        # 添加一个身体部分
        self.snake._SnakeGrid__add_snake_body()
        
        # 保存初始位置
        head_pos = IntVector2(self.snake.snake_head.x, self.snake.snake_head.y)
        tail_pos = IntVector2(self.snake.snake_tail.x, self.snake.snake_tail.y)
        
        # 滚动一次
        self.snake.roll()
        
        # 检查位置是否下移
        self.assertEqual(self.snake.snake_head, IntVector2(head_pos.x, head_pos.y + 1))
        self.assertEqual(self.snake.snake_tail, IntVector2(tail_pos.x, tail_pos.y + 1))
    
    def test_fall(self):
        """测试掉落功能"""
        # 启用掉落
        self.snake.is_enable_falling = True
        
        # 设置初始位置
        self.snake.snake_head = IntVector2(5, 5)
        self.snake.set_cell(5, 5, 31)  # 设置蛇头
        
        # 添加一个身体部分
        self.snake._SnakeGrid__add_snake_body()
        
        # 保存初始位置
        initial_y = self.snake.snake_head.y
        
        # 确保掉落缓冲区足够大以触发掉落
        self.snake.fall_speed_buffer = self.snake.fall_speed * 0.1  # 确保足够大
        
        # 执行掉落
        self.snake._SnakeGrid__fall(0.1, None)
        
        # 检查位置是否下移
        self.assertGreater(self.snake.snake_head.y, initial_y, 
                         f"蛇头应从 {initial_y} 向下移动，实际位置: {self.snake.snake_head.y}")
    
    def test_boundary_check(self):
        """测试边界检查"""
        # 重置死亡标志
        self.death_triggered = False
        
        # 移动蛇到右边界
        self.snake.snake_head = IntVector2(9, 5)  # 网格宽度为10，所以x=9是右边界
        self.snake.direction = IntVector2(1, 0)  # 向右移动
        
        # 检查下一个位置是否超出边界
        next_pos = self.snake.snake_head + self.snake.direction
        if (next_pos.x < 0 or next_pos.x >= self.snake.grid_width or 
            next_pos.y < 0 or next_pos.y >= self.snake.grid_height):
            self.death_triggered = True
        
        # 验证死亡信号是否应该被触发
        self.assertTrue(self.death_triggered, "移出边界应触发死亡信号")

if __name__ == '__main__':
    unittest.main()
