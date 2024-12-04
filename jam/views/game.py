from arcade import camera

from jam.core.application import View
from jam.core.map import Planet
from jam.core.context import context

from jam.lib.fly import FlyAroundGrip

class GameView(View):

    def __init__(self) -> None:
        super().__init__()
        self.planet: Planet = None
        self.perspective_camera = camera.PerspectiveProjector()
        self.perspective_camera.view.position = (0.0, 0.0, -200.0)
        self.perspective_camera.projection.far = 5000.0
        
        self.fly_grip = FlyAroundGrip(self.perspective_camera.view)

    def on_key_press(self, symbol, modifiers): self.fly_grip.press(symbol, modifiers)
    def on_key_release(self, symbol, modifiers): self.fly_grip.release(symbol, modifiers)
    def on_mouse_motion(self, x, y, dx, dy): self.fly_grip.look(x, y, dx, dy)
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y): self.fly_grip.zoom(scroll_y)

    def on_show_view(self):
        self.planet = Planet(context.player.size, context.player.noise)
        self.planet.renderer.render_mesh = False

    def on_draw(self) -> None:
        self.clear()
        with self.perspective_camera.activate():
            self.planet.draw()

    def on_update(self, delta_time):
        self.fly_grip.update(delta_time)
