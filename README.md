# pygame-game-design

## 项目简介
pygame-game-design 是一个基于 Pygame 的简单游戏框架，专为游戏策划课程的大作业设计的原型开发工具。框架旨在帮助开发者快速构建游戏原型，提供了基本的游戏循环、玩家对象模板以及工具函数，便于扩展和定制。

## 文件结构
- **main.py**  
  游戏运行入口，负责初始化游戏实例并启动游戏循环。
  
- **game.py**  
  游戏循环实例，包含 `Game` 类，负责管理游戏的主循环、事件处理、状态更新和绘制逻辑。
  
- **gameObject/player.py**  
  玩家类模板，包含 `Player` 类，负责玩家的初始化、状态更新和绘制。
  
- **gameObject/SpriteSheet.py**  
  图集加载器，提供切分图集的功能，支持规则网格、连续排列和自定义切分。

- **tools.py**  
  工具模块，包含加载图像和音效的辅助函数。

- **assets/**  
  - **images/** 存放游戏所需的图片资源。
  - **musics/** 存放游戏所需的音效资源。

- **duc/**  
  - **游戏框架.md** 游戏框架的设计规范和文件说明。
  - **个人Pygame理解.md** 关于 Pygame 的个人学习笔记。

- **test/**  
  测试模块，用于测试游戏功能。

## 游戏框架设计
游戏框架的核心是 `Game` 类，负责管理游戏的生命周期。所有游戏对象需实现以下方法：
- `__init__()` 初始化方法，定义对象属性和数据。
- `update(delta_time)` 更新方法，更新对象状态。
- `draw(screen)` 绘制方法，绘制对象到屏幕。

游戏对象的更新和绘制由 `Game` 类统一管理，确保逻辑清晰、职责分离。

## 快速开始
1. 确保已安装 Python 和 Pygame。
2. 克隆项目到本地：
   ```bash
   git clone <repository-url>
   ```
3. 安装依赖：
   ```bash
   pip install pygame
   ```
4. 运行游戏：
   ```bash
   python main.py
   ```

## 适用场景
- 游戏策划课程的原型开发。
- 学习和实践 Pygame 的基础知识。
- 快速搭建 2D 游戏框架，便于扩展和定制。

## 参考
- [Pygame 官方文档](https://www.pygame.org/docs/)
