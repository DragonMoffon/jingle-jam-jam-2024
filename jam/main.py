from jam.core.application import Window
from jam.views.root import RootView

from jam.core.context import context

def main() -> None:
    win = Window()
    context.set_window(win)

    root = RootView()

    win.show_view(root)
    win.run()
