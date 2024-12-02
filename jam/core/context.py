from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jam.core.application import Window

class GameContext:
    TITLE: str = 'jingle jam'
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 720
    
    def __init__(self):
        self.window: Window = None

    def set_window(self, window: Window):
        if self.window is not None:
            raise ValueError('Window already set')
        self.window = window
context = GameContext()


class PlayerContext:
    pass