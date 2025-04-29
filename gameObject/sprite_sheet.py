import pygame
from typing import List, Dict, Optional, Union

class SpriteSheet:
    def __init__(self, filename: str):
        """
        初始化图集加载器
        :param filename: 图集文件路径
        """
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            raise SystemExit(f"无法加载图集 {filename}: {e}")

    def get_image(self, x: int, y: int, width: int, height: int) -> pygame.Surface:
        """
        从图集中切分单个素材
        :param x: 左上角x坐标
        :param y: 左上角y坐标
        :param width: 素材宽度
        :param height: 素材高度
        :return: 切分后的Surface对象
        """
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

    def load_grid(
        self, 
        tile_width: int, 
        tile_height: int, 
        margin: int = 0, 
        spacing: int = 0
    ) -> List[pygame.Surface]:
        """
        自动切分规则网格排列的图集
        :param tile_width: 每个素材的宽度
        :param tile_height: 每个素材的高度
        :param margin: 图集外边框宽度（可选）
        :param spacing: 素材之间的间隔（可选）
        :return: 切分后的素材列表
        """
        sprites = []
        sheet_width, sheet_height = self.sheet.get_size()
        
        for y in range(margin, sheet_height - margin, tile_height + spacing):
            for x in range(margin, sheet_width - margin, tile_width + spacing):
                sprites.append(self.get_image(x, y, tile_width, tile_height))
        
        return sprites

    def load_strip(
        self, 
        rect: pygame.Rect, 
        image_count: int, 
        horizontal: bool = True
    ) -> List[pygame.Surface]:
        """
        切分连续排列的素材（如动画帧）
        :param rect: 第一帧的矩形区域 (x, y, width, height)
        :param image_count: 素材数量
        :param horizontal: 是否水平排列（默认True）
        :return: 切分后的素材列表
        """
        images = []
        x, y, width, height = rect

        for i in range(image_count):
            if horizontal:
                images.append(self.get_image(x + i * width, y, width, height))
            else:
                images.append(self.get_image(x, y + i * height, width, height))
        
        return images

    def load_custom(self, rects: List[Union[pygame.Rect, tuple]]) -> List[pygame.Surface]:
        """
        自定义切分不规则排列的素材
        :param rects: 矩形区域列表，每个元素为 (x, y, width, height) 或 pygame.Rect
        :return: 切分后的素材列表
        """
        return [self.get_image(*rect) if isinstance(rect, tuple) else self.get_image(*rect.topleft, rect.width, rect.height) 
                for rect in rects]