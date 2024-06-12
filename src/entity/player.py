from math import atan2, pi

from src.bounds.bcircle import BCircle
from src.entity.character import Character
from src.util.controls import controls


class Player(Character):
    def __init__(self, config):
        super().__init__(config)

        self.is_walking = False
        self.is_shooting = False
        self.used_ammo = 0
        self.score = 0
        self.kills = 0
        self.kills_ratio = self.calculate_kills_ratio()
        self.pickup_zone = BCircle(self.position, 1.5)
        self.want_to_grab = False
        self.grabbed_item = False

    def increase_hp(self, val: int):
        self.health = max(0, self.health - val)

        if self.health == 0:
            self.is_dead = True

    def heal(self, heal_scale: float):
        self.health = min(100, self.health + int(self.health * heal_scale))

    def draw(self):
        pass
        # self.sprite.update(640, 360, 0.0, self.rotation, 2.0)
        # self.sprite.draw()

    def increment_score(self, new_score: int):
        self.score += new_score

    def increment_kills(self):
        self.kills += 1

    def increment_ammo_usage(self, ammo_amount: int):
        self.used_ammo += ammo_amount

    def calculate_kills_ratio(self):
        return self.kills / self.used_ammo if self.used_ammo > 0 else 0

    def react_to_control(self):
        self.is_walking = False

        if controls.get_bind('move_up'):
            self.velocity.y = self.move_speed
            self.is_walking = True

        if controls.get_bind('move_right'):
            self.velocity.x = self.move_speed
            self.is_walking = True

        if controls.get_bind('move_down'):
            self.velocity.y = -self.move_speed
            self.is_walking = True

        if controls.get_bind('move_left'):
            self.velocity.x = -self.move_speed
            self.is_walking = True

        use_item_pressed = controls.get_bind('use_item')

        if use_item_pressed and not self.is_shooting:
            print('start shoot')
            if self.weapon is not None:
                self.weapon.start_use()
                self.is_shooting = True
        if not use_item_pressed and self.is_shooting:
            print('stop shoot')
            if self.weapon is not None:
                self.weapon.stop_use()
                self.is_shooting = False

        grab_item_pressed = controls.get_bind('grab_item')
        if grab_item_pressed:
            self.want_to_grab = True
        else:
            self.want_to_grab = False
            self.grabbed_item = False

        x_change_mouse_player = controls.mouse_x - 640
        y_change_mouse_player = controls.mouse_y - 360
        self.rotation = atan2(y_change_mouse_player, x_change_mouse_player) - pi / 2

    def update(self, delta_time):
        self.time += delta_time
        self.update_motion(delta_time)
        self.react_to_control()
        self.update_weapon_offset()
        self.pickup_zone.center = self.position
