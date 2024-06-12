from math import cos, sin

from pyglet.math import Vec3

from src.entity.entity import Entity


class Projectile(Entity):
    def __init__(self, config, tracer_rect_proto):
        super().__init__()
        self.get_velocity_loss = self.get_projectile_drag

        self.initial_velocity = config.get('velocity') / 10
        self.pellets = config.get('pellets', 1)
        self.remove_time = config.get('remove_time', 10)
        self.base_spread = config.get('base_spread', 0)
        self.base_damage = config.get('hit', {}).get('base_damage')

        self.rect = tracer_rect_proto.create_mesh(self.position, 0, Vec3(0.75, 0.75, 0.75))

        # TODO add hit and explosion property
        # TODO spread, damage dealt

    def shoot(self, rotation):
        self.velocity.x = -sin(rotation) * self.initial_velocity
        self.velocity.y = cos(rotation) * self.initial_velocity
        self.rotation = rotation

    def update(self, delta_time):
        self.update_motion(delta_time)
        self.rect.position = self.position
        self.rect.rotation = self.rotation
