from game import Game
import tools
import gameObject.game_map_manager

if __name__ == "__main__":
    # 创建游戏实例
    game = Game((900.0, 900.0))  # 屏幕大小和玩家初始位置

    try:
        # 设置窗口图标和背景
        game.set_window_icon("assets/images/icon.png")
        game.load_background("assets/images/back.png")

        # 创建地图管理器实例
        gameMap = gameObject.game_map_manager.GameMapManager(cell_size=20)  # 创建地图管理器实例
        gameMap.load_level("level/level_test40x40.csv", read_row_count=20)
        gameMap.set_map_scrolling(True)
        gameMap.roll_speed = 1

        # 设置蛇属性
        gameMap.set_snake_is_enable_falling(True)  # 设置蛇允许掉落
        gameMap.snake_grid.set_snake_art(tools.load_image("snake_head.png"), tools.load_image("snake_body.png"), tools.load_image("snake_tail.png"))

        # 添加地图管理器
        game.addGameObject(gameMap)  # 添加地图管理器

        # 运行游戏
        game.run()  # 运行游戏
    finally:
        game.quit()  # 确保退出时清理资源