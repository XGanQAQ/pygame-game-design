from .ui_canvas import UICanvas
from pygame.math import Vector2
from typing import Union
import pygame_gui
import pygame
from game import LifeCycle, Game

class EndGameUICanvas(UICanvas):
    def __init__(self,screen_size: Union[tuple, Vector2] = (1600, 900), theme_path: str = "theme.json", game_map_manager = None):
        super().__init__(screen_size, theme_path)

        self.game_map_manager = game_map_manager

        self.end_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((500, 300), (600, 50)),
            text="You Die !!!!",
            manager=self.ui_manager,
            object_id="#end_label",
        )

        self.end_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 400), (600, 50)),
            text="Restart",
            manager=self.ui_manager,
            object_id="#end_button",
        )

        Game._instance.signals[LifeCycle.GAME_OVER].connect(self.show)
        self.hide(self)

    def show(self, sender):
        self.end_label.show()
        self.end_button.show()

    def hide(self, sender):
        self.end_label.hide()
        self.end_button.hide()

    def init(self, sender, **kwargs):
        super().init(sender, **kwargs)
    
    def update(self, sender, **kwargs):
        super().update(sender, **kwargs)
    
    def event(self, sender, **kwargs):
        super().event(sender, **kwargs)
        if kwargs.get("event", None).type == pygame.USEREVENT:
            if kwargs.get("event", None).user_type == pygame_gui.UI_BUTTON_PRESSED:
                if kwargs.get("event", None).ui_element == self.end_button:
                    Game._instance.game_resume(self)
                    self.hide(self)
    
    def draw(self, sender, **kwargs):
        super().draw(sender, **kwargs)
    
    