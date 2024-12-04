from arcade.camera import CameraData, grips
from arcade.math import quaternion_rotation
from arcade import key, Vec2

from jam.core.context import PlayerContext


class FlyAroundGrip:

    def __init__(self, data: CameraData):
        self._camera_data: CameraData = data

        self._forward_velocity: float = 0.0

        self._strafe_vertical: int = 0
        self._strafe_horizontal: int = 0
        self._accelerate_forward: int = 0
        self._roll_velocity: int = 0
        self._pitch_velocity: float = 0.0
        self._yaw_velocity: float = 0.0

        self._pitch: float = 0.0
        self._yaw: float = 0.0

        self._global_up = (0.0, 1.0, 0.0)

    def look(self, x: int, y: int, dx: int, dy: int):
        self._yaw_velocity = dx
        self._pitch_velocity = -dy

    def zoom(self, dy):
        if dy > 0:
            self._camera_data.zoom = max(min(self._camera_data.zoom * 1.25, 2.0), 0.5)
        elif dy < 0:
            self._camera_data.zoom = max(min(self._camera_data.zoom / 1.25, 2.0), 0.5)

    def press(self, symbol, modifier):
        match symbol:
            case key.SPACE:
                self._strafe_vertical += 1
            case key.LSHIFT:
                self._strafe_vertical -= 1
            case key.W:
                self._accelerate_forward += 1
            case key.S:
                self._accelerate_forward -= 1
            case key.A:
                self._strafe_horizontal -= 1
            case key.D:
                self._strafe_horizontal += 1
            case key.Q:
                self._roll_velocity += 1
            case key.E:
                self._roll_velocity -= 1

    def release(self, symbol, modifier):
        match symbol:
            case key.SPACE:
                self._strafe_vertical -= 1
            case key.LSHIFT:
                self._strafe_vertical += 1
            case key.W:
                self._accelerate_forward -= 1
            case key.S:
                self._accelerate_forward += 1
            case key.A:
                self._strafe_horizontal += 1
            case key.D:
                self._strafe_horizontal -= 1
            case key.Q:
                self._roll_velocity -= 1
            case key.E:
                self._roll_velocity += 1

    def update(self, dt: float):
        camera = self._camera_data

        if self._pitch_velocity or self._yaw_velocity:
            self._pitch = min(
                max(self._pitch + PlayerContext.LOOK_SENSITIVITY * dt * self._pitch_velocity, -89.0),
                89.0,
            )
            self._yaw = (self._yaw + PlayerContext.LOOK_SENSITIVITY * dt * self._yaw_velocity) % 360

            camera.up = self._global_up
            camera.forward = quaternion_rotation(
                self._global_up, (0.0, 0.0, -1.0), self._yaw
            )
            camera.up, camera.forward = grips.rotate_around_right(camera, self._pitch)

            self._pitch_velocity = 0.0
            self._yaw_velocity = 0.0

        if self._accelerate_forward:
            o_pos = camera.position
            fw = camera.forward
            fw_speed = PlayerContext.MOVE_SPEED * self._accelerate_forward * dt
            camera.position = (
                o_pos[0] + fw_speed * fw[0],
                o_pos[1] + fw_speed * fw[1],
                o_pos[2] + fw_speed * fw[2],
            )

        if self._strafe_vertical or self._strafe_horizontal:
            self._strafe_vertical = min(1, max(-1, self._strafe_vertical))
            self._strafe_horizontal = min(1, max(-1, self._strafe_horizontal))
            strafe = (
                Vec2(self._strafe_horizontal, self._strafe_vertical).normalize()
                * PlayerContext.MOVE_SPEED
                * dt
            )
            camera.position = grips.strafe(camera, strafe)

    def select(self):
        self._accelerate_forward = 0
        self._pitch_velocity = 0
        self._yaw_velocity = 0
        self._roll_velocity = 0

