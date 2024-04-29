from math import atan2

from pyglet.sprite import Sprite

from src.entity.entity import Entity
from src.frame.frame import Frame
from src.util.controls import Controls


class Player(Entity):
    def __init__(self, initial_frame: Frame):
        super().__init__()
        self.sprite: Sprite = initial_frame.sprite
        self.rect = None
        self.drag = 20
        self.player_speed = 0.25
        self.is_walking = False

    def draw(self):
        self.sprite.update(640, 360, 0.0, self.rotation, 2.0)
        self.sprite.draw()

    def react_to_control(self):
        controls = Controls.default()
        self.is_walking = False

        if controls.get_bind('move_up'):
            self.velocity.y = self.player_speed
            self.is_walking = True

        if controls.get_bind('move_right'):
            self.velocity.x = self.player_speed
            self.is_walking = True

        if controls.get_bind('move_down'):
            self.velocity.y = -self.player_speed
            self.is_walking = True

        if controls.get_bind('move_left'):
            self.velocity.x = -self.player_speed
            self.is_walking = True

        x_change_mouse_player = controls.mouse_x - 640
        y_change_mouse_player = controls.mouse_y - 360
        self.rotation = -atan2(y_change_mouse_player, x_change_mouse_player) * 60

    def update(self, delta_time):
        self.time += delta_time
        self.update_motion(delta_time)
        self.react_to_control()
