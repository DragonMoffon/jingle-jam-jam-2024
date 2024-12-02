from array import array
from jam.core.application import View
import arcade.gl as gl


def gen_spiral():
    pass

class SpiralView(View):

    def __init__(self) -> None:
        super().__init__()

    def on_draw(self) -> None:
        self.clear()
