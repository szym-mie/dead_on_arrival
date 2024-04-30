from math import cos, sin, pi

from src.entity.entity import Entity


class Projectile(Entity):
    def __init__(self, initial_frame, x, y, angle):
        super().__init__()
        self.sprite = initial_frame.sprite
        self.get_velocity_loss = self.get_projectile_drag
        self.rect = None
        self.position.x = x
        self.position.y = y
        self.angle = angle
        self.speed = 25
        self.velocity.x = cos(self.angle*(2*pi/360))*self.speed
        self.velocity.y = sin(self.angle*(2*pi/360))*self.speed

    def move(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    def update(self, delta_time):
        self.move()
        self.update_motion(delta_time)

    def draw(self):
        self.sprite.update(self.position.x + 640, self.position.y + 360, 0, -self.angle, 2.0)
        self.sprite.draw()
