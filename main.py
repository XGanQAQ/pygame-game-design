from game import Game
import tools
import gameObject.game_map_manager
import gameObject.ui.start_game_ui_canvas as ui
from game import LifeCycle

if __name__ == "__main__":
    # 创建游戏实例
    game = Game((1600.0, 900.0))  # 屏幕大小和玩家初始位置

    try:
        # 设置窗口图标和背景
        game.set_window_icon("assets/images/icon.png")
        game.load_background("assets/images/back_all.jpg")

        # 创建地图管理器实例
        gameMap = gameObject.game_map_manager.GameMapManager(cell_size=25, map_background=tools.load_image("back.png"))  # 创建地图管理器实例
        gameMap.load_level("level/level_test_36x20.csv", read_row_count=20)
        gameMap.set_map_scrolling(True)
        gameMap.roll_speed = 1

        # 设置蛇属性
        gameMap.set_snake_is_enable_falling(True)  # 设置蛇允许掉落
        gameMap.snake_grid.set_snake_art(tools.load_image("snake_head.png"), tools.load_image("snake_body.png"), tools.load_image("snake_tail.png"))

        # 添加游戏开始信号
        game.signals[LifeCycle.GAME_START].connect(gameMap.set_game_start)

        # 添加地图管理器
        game.addGameObject(gameMap)  # 添加地图管理器

        # 添加UI
        start_game_ui = ui.StartGameUICanvas((1600, 900))
        game.addGameObject(start_game_ui)

        # 初始化游戏对象
        game.init_game_objects()

        # 运行游戏
        game.run()  # 运行游戏
    finally:
        game.quit()  # 确保退出时清理资源