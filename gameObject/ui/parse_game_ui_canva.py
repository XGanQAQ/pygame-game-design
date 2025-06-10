from .ui_canvas import UICanvas
from pygame.math import Vector2
from typing import Union
import pygame_gui
import pygame
from game import LifeCycle, Game

class ParseGameUICanvas(UICanvas):
    def __init__(self,screen_size: Union[tuple, Vector2] = (1600, 900), theme_path: str = "theme.json", game_map_manager = None):
        super().__init__(screen_size, theme_path)

        self.game_map_manager = game_map_manager

        self.parse_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((500, 600), (600, 50)),
            text="Parse Game",
            manager=self.ui_manager,
            object_id="#parse_label",
        )

        self.parse_label.hide()

    def init(self, sender, **kwargs):
        super().init(sender, **kwargs)
    
    def update(self, sender, **kwargs):
        super().update(sender, **kwargs)
    
    def event(self, sender, **kwargs):
        super().event(sender, **kwargs)
        if kwargs.get("event", None).type == pygame.KEYDOWN:
            if kwargs.get("event", None).key == pygame.K_ESCAPE:
                Game._instance.game_pause(self)
    
    def draw(self, sender, **kwargs):
        super().draw(sender, **kwargs)
    
    def on_game_start(self, sender):
        self.parse_label.hide()

    def on_game_pause(self, sender):
        self.parse_label.show()

    def on_game_resume(self, sender):
        self.parse_label.hide()
    