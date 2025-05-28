from game import Game
import gameObject.game_map_manager

if __name__ == "__main__":
    # 创建游戏实例
    game = Game((1600.0, 900.0))  # 屏幕大小和玩家初始位置

    try:
        gameMap = gameObject.game_map_manager.GameMapManager(cell_size=20)  # 创建地图管理器实例
        gameMap.load_level("level/level_test40x40.txt")
        gameMap.set_snake_is_enable_falling(True)  # 设置蛇允许掉落
        game.addGameObject(gameMap)  # 添加地图管理器
        game.run()  # 运行游戏
    finally:
        game.quit()  # 确保退出时清理资源