from abc import ABC, abstractmethod

class GameObject(ABC):
    """
    GameObject is the base class for all game objects in the game.
    It provides a common interface for initialization, update, and drawing.
    """
    def __init__(self):
        self.initialized = False  # 标记是否已初始化

    def init(self):
        """
        Initialize the game object.
        This method should be overridden by subclasses.
        """
        if not self.initialized:
            self.initialized = True
            print(f"{self.__class__.__name__} initialized.")

    @abstractmethod
    def update(self, delta_time):
        """
        Update the game object.
        This method should be overridden by subclasses.
        """
        pass

    @abstractmethod
    def draw(self, screen):
        """
        Draw the game object on the screen.
        This method should be overridden by subclasses.
        """
        pass