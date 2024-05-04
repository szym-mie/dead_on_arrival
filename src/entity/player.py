from math import atan2, inf, pi

from pyglet.math import Vec2
from pyglet.sprite import Sprite

from src.bounds.bcircle import BCircle
from src.entity.entity import Entity
from src.entity.projectile import Projectile
from src.entity.ranged_weapon import RangedWeapon
from src.frame.frame import Frame
from src.util.controls import Controls


class Player(Entity):
    def __init__(self, initial_frame: Frame, bullet_initial_frame: Frame, level):
        super().__init__()
        self.sprite: Sprite = initial_frame.sprite
        self.bullet_initial_frame = bullet_initial_frame
        self.level = level
        self.rect = None
        self.drag = 20
        self.player_speed = 0.25
        self.is_walking = False
        self.is_shooting = False
        self.current_weapon = RangedWeapon(name="conda", ammo=inf, damage=5, usage_cooldown=10, weapon_offset=Vec2(0, -1))
        self.used_ammo = 0
        self.score = 0
        self.kills = 0
        self.kills_ratio = self.calculate_kills_ratio()
        self.health_point = 100
        self.is_dead = False
        self.bullet_group = []
        self.pickup_zone = BCircle(self.position, 1)

    def increase_hp(self, val: int):
        self.health_point = max(0, self.health_point - val)

        if self.health_point == 0:
            self.is_dead = True

    def heal(self, heal_scale: float):
        self.health_point = min(100, self.health_point + int(self.health_point * heal_scale))

    def draw(self):
        self.sprite.update(640, 360, 0.0, self.rotation, 2.0)
        self.sprite.draw()

    def increment_score(self, new_score: int):
        self.score += new_score

    def increment_kills(self):
        self.kills += 1

    def increment_ammo_usage(self, ammo_amount: int):
        self.used_ammo += ammo_amount

    def calculate_kills_ratio(self):
        return self.kills / self.used_ammo if self.used_ammo > 0 else 0

    def attack(self):
        if self.current_weapon.usage_cooldown == 0 and self.current_weapon.ammo > 0:
            print(f'shooting')
            self.current_weapon.usage_cooldown = 10
            spawn_bullet_pos = Vec2(1, -0.3).rotate(-self.rotation / 360 * 2 * pi)
            # spawn_bullet_pos =
            print(f'{spawn_bullet_pos=}')
            projectile = Projectile(self.bullet_initial_frame, spawn_bullet_pos.x * 64, spawn_bullet_pos.y * 64, -self.rotation, self.level)
            self.bullet_group.append(projectile)

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

        if controls.get_bind("fire_weapon"):
            self.attack()
            self.is_shooting = True

        x_change_mouse_player = controls.mouse_x - 640
        y_change_mouse_player = controls.mouse_y - 360
        self.rotation = -atan2(y_change_mouse_player, x_change_mouse_player) * 180 / pi

    def update(self, delta_time):
        self.time += delta_time
        self.update_motion(delta_time)
        self.react_to_control()
        if self.current_weapon.usage_cooldown > 0:
            self.current_weapon.usage_cooldown -= 1

        for bullet in self.bullet_group:
            if self.level.get_tile_at(bullet.position.x, bullet.position.y) == 0:
                del self

