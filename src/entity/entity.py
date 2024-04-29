from abc import abstractmethod, ABC

from pyglet.math import Vec2


class Entity(ABC):
    def __init__(self):
        self.position = Vec2()
        self.velocity = Vec2()
        self.rotation = 0
        self.drag = 1
        self.get_velocity_loss = self.get_entity_drag
        self.time = 0

    def get_item_drag(self, delta_time):
        return self.drag * delta_time

    def get_entity_drag(self, delta_time):
        return self.drag * self.velocity.mag * delta_time

    def get_projectile_drag(self, delta_time):
        return self.drag * self.velocity.mag * pow(delta_time, 2)

    def update_motion(self, delta_time):
        e = 0.00001

        if self.velocity.mag > e:
            last_magnitude = self.velocity.mag
            next_magnitude = max(last_magnitude - self.get_velocity_loss(delta_time), 0)
            scale = next_magnitude / last_magnitude
            self.velocity *= scale
            self.position += self.velocity

    def update(self, delta_time):
        self.time += delta_time
        self.update_motion(delta_time)
