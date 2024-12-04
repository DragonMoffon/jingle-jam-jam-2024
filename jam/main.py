from jam.core.application import Window
from jam.views.game import GameView

from jam.core.context import context

def main() -> None:
    win = Window()
    context.initialise(win)

    root = GameView()

    win.show_view(root)
    win.run()
