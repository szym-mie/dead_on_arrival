from dataclasses import dataclass


@dataclass
class Rectangle:
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    def intersect(self, other):
        return Rectangle(max(self.x1, other.x1), max(self.y1, other.y1),
                         min(self.x2, other.x2), min(self.y2, other.y2))

    def collides(self, other) -> bool:
        return not (self.x2 < other.x1 or self.y2 < other.y1 or
                    self.x1 > other.x2 or self.y1 > other.y2)

    @classmethod
    def from_sprite(cls,sprite):
        x = int(sprite.x - sprite.image.anchor_x)
        y = int(sprite.y - sprite.image.anchor_y)
        return cls(x, y, x + sprite.width, y + sprite.height)
