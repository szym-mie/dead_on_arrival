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
        self.pickup_zone = BCircle(self.position, 1)

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

    def attack(self):
        pass
        # if self.current_weapon.usage_cooldown == 0 and self.current_weapon.ammo > 0:
        #     print(f'shooting')
        #     self.current_weapon.usage_cooldown = 10
        #     spawn_bullet_pos = Vec2(1, -0.3).rotate(-self.rotation / 360 * 2 * pi)
        #     # spawn_bullet_pos =
        #     print(f'{spawn_bullet_pos=}')
        #     projectile = Projectile(self.bullet_initial_frame, spawn_bullet_pos.x * 64, spawn_bullet_pos.y * 64, -self.rotation, self.level)
        #     self.bullet_group.append(projectile)

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

        if controls.get_bind("fire_weapon"):
            self.attack()
            self.is_shooting = True

        x_change_mouse_player = controls.mouse_x - 640
        y_change_mouse_player = controls.mouse_y - 360
        self.rotation = atan2(y_change_mouse_player, x_change_mouse_player) - pi / 2

    def update(self, delta_time):
        self.time += delta_time
        self.update_motion(delta_time)
        self.react_to_control()
        self.update_weapon_offset()
