from arcade import View as ArcadeView, Window as ArcadeWindow
from jam.core.context import context

# Update these classes if you want custom functionality in your Windows and Views.

__all__ = (
    'Window',
    'View',
    'ArcadeWindow',
    'ArcadeView'
)

class Window(ArcadeWindow):

    def __init__(self):
        super().__init__(context.WINDOW_WIDTH, context.WINDOW_HEIGHT, context.TITLE)


class View(ArcadeView):

    def __init__(self, window: Window | None = None) -> None:
        super().__init__(window)
