from .ui_canvas import UICanvas
from pygame.math import Vector2
from typing import Union
import pygame_gui
import pygame

class StartGameUICanvas(UICanvas):
    def __init__(self,screen_size: Union[tuple, Vector2] = (1600, 900)):
        super().__init__(screen_size)

        self.begin_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 200), (200, 50)),
            text="Click To Begin",
            manager=self.ui_manager,
        )


    def init(self, sender, **kwargs):
        super().init(sender, **kwargs)
        
    def update(self, sender, **kwargs):
        super().update(sender, **kwargs)
    
    def event(self, sender, **kwargs):
        super().event(sender, **kwargs)
    
    def draw(self, sender, **kwargs):
        super().draw(sender, **kwargs)
    
    