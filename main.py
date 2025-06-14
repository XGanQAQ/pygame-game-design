from game import Game
import tools
import gameObject.game_map_manager
import gameObject.ui.start_game_ui_canva
import gameObject.ui.end_game_ui_canva
import gameObject.ui.parse_game_ui_canva
from gameObject.audio_manager import AudioManager
from game import LifeCycle

if __name__ == "__main__":
    # 创建游戏实例
    game = Game((1600.0, 900.0))  # 屏幕大小和玩家初始位置
    audio = AudioManager()

    try:
        # 设置窗口图标和背景
        game.set_window_icon(tools.load_image("icon.png"))

        # 创建实例
        # 创建地图管理器实例
        gameMap = gameObject.game_map_manager.GameMapManager(cell_size=25, map_gameplay=tools.load_image("back.png"), screen_size=(1600, 900))  # 创建地图管理器实例
        
        # 加载地图
        gameMap.load_level("level/level_first_36x396_0.1.0.csv", read_row_count=20)
        gameMap.load_map_background("back_all.jpg")
        gameMap.set_map_scrolling(True)
        gameMap.roll_speed = 1

        # 设置蛇属性
        gameMap.set_snake_is_enable_falling(True)  # 设置蛇允许掉落
        gameMap.snake_grid.snake.snak_dead_signal.connect(game.game_over)

        # 添加游戏开始信号
        game.signals[LifeCycle.GAME_START].connect(gameMap.on_game_start)
        game.signals[LifeCycle.GAME_PAUSE].connect(gameMap.on_game_pause)
        game.signals[LifeCycle.GAME_RESUME].connect(gameMap.on_game_resume)
        game.signals[LifeCycle.GAME_OVER].connect(gameMap.on_game_over)
        
        # 添加地图管理器
        game.addGameObject(gameMap)  # 添加地图管理器

        # 添加UI
        start_game_ui = gameObject.ui.start_game_ui_canva.StartGameUICanvas((1600, 900), game_map_manager=gameMap)
        game.addUI(start_game_ui)
        game.signals[LifeCycle.GAME_START].connect(start_game_ui.on_game_start)
        game.signals[LifeCycle.GAME_PAUSE].connect(start_game_ui.on_game_pause)
        game.signals[LifeCycle.GAME_RESUME].connect(start_game_ui.on_game_resume)

        end_game_ui = gameObject.ui.end_game_ui_canva.EndGameUICanvas((1600, 900), game_map_manager=gameMap)
        game.addUI(end_game_ui)
        game.signals[LifeCycle.GAME_OVER].connect(end_game_ui.on_game_over)
        game.signals[LifeCycle.GAME_RESUME].connect(end_game_ui.on_game_resume)

        parse_game_ui = gameObject.ui.parse_game_ui_canva.ParseGameUICanvas((1600, 900), game_map_manager=gameMap)
        game.addUI(parse_game_ui)
        game.signals[LifeCycle.GAME_START].connect(parse_game_ui.on_game_start)
        game.signals[LifeCycle.GAME_PAUSE].connect(parse_game_ui.on_game_pause)
        game.signals[LifeCycle.GAME_RESUME].connect(parse_game_ui.on_game_resume)

        # 初始化游戏对象
        game.init_game_objects()

        audio.playMusic("maou_bgm_8bit27")


        # 运行游戏
        game.run()  # 运行游戏
    finally:
        game.quit()  # 确保退出时清理资源