from __future__ import annotations
from typing import TYPE_CHECKING

from jam.core.map import PlanetSize, PlanetNoise

if TYPE_CHECKING:
    from jam.core.application import Window


class PlayerContext:
    LOOK_SENSITIVITY: float = 60.0
    ROLL_SPEED: float = 60.0
    MOVE_SPEED: float = 60.0

    def __init__(self):
        self.size: PlanetSize = PlanetSize.MEDIUM
        self.noise: PlanetNoise = PlanetNoise.MEDIUM


class GameContext:
    TITLE: str = 'jingle jam'
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 720
    MOUSE_EXCLUSIVE: bool = True
    MOUSE_SHOWN: bool = False
    
    def __init__(self):
        self.window: Window = None
        self.player: PlayerContext = None

    def set_window(self, window: Window):
        if self.window is not None:
            raise ValueError('Window already set')
        self.window = window

    def initialise(self, window: Window):
        self.set_window(window)
        window.set_exclusive_mouse(GameContext.MOUSE_EXCLUSIVE)
        window.set_mouse_visible(GameContext.MOUSE_SHOWN)
        self.player = PlayerContext()
context = GameContext()
