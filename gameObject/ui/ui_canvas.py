import pygame_gui
import pygame
from ..game_object import GameObject
from typing import Union
from pygame.math import Vector2

class UICanvas(GameObject):
    def __init__(self,screen_size: Union[tuple, Vector2] = (1600, 900), theme_path: str = "theme.json"):
        super().__init__()
        self.ui_manager = pygame_gui.UIManager(screen_size, theme_path)
        self.screen_size = screen_size
        self.font = None
        self.font_size = None
        pass

    def init(self, sender, **kwargs):
        super().init(sender, **kwargs)

    def update(self, sender, **kwargs):
        super().update(sender, **kwargs)
        self.ui_manager.update(kwargs.get("delta_time", 0))

    def event(self, sender, **kwargs):
        super().event(sender, **kwargs)
        self.ui_manager.process_events(kwargs.get("event", None))

    def draw(self, sender, **kwargs):
        super().draw(sender, **kwargs)
        self.ui_manager.draw_ui(kwargs.get("screen", None))

    def set_theme(self, theme_path: str):
        self.ui_manager.get_theme().load_theme(theme_path)