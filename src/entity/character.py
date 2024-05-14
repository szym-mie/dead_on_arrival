from math import cos, sin

from pyglet.math import Vec3

from src.entity.entity import Entity


class Character(Entity):
    # TODO use dict.get to retrieve values without KeyErrors

    def __init__(self, config):
        super().__init__()

        self.weapon = None
        self.weapon_position = Vec3()

        self.drag = 20

        self.health_max = config['hp']
        self.armor_max = config['ap']

        self.health = self.health_max
        self.armor = self.armor_max

        self.move_speed = config['move_speed']

        self.frames = config['anim']

        self.is_dead = False

    def update_weapon_offset(self):
        if self.weapon is not None:
            weapon_offset = Vec3(0.3, 0.5, 0.0)
            # weapon_offset = self.weapon.offset

            weapon_offset_rotated = Vec3(
                cos(-self.rotation) * weapon_offset.x + sin(-self.rotation) * weapon_offset.y,
                -sin(-self.rotation) * weapon_offset.x + cos(-self.rotation) * weapon_offset.y,
                0.0
            )
            self.weapon_position = self.position + weapon_offset_rotated

