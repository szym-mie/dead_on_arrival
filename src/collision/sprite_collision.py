import weakref
from typing import Any
from src.collision.rectangle import Rectangle
image_data_cache = weakref.WeakKeyDictionary()


class SpriteCollision:
    def __init__(self, sprite):
        self.sprite = sprite

    def get_image(self) -> tuple[Any, Any, Any]:
        image = self.sprite.image
        if image in image_data_cache:
            d = image_data_cache[image]
        else:
            d = image.get_image_data().get_data('A', image.width)
            image_data_cache[image] = d
        return d, image.width, image.height

    def get_rect(self) -> Rectangle:
        return Rectangle.from_sprite(self.sprite)


def collide(sprite1, sprite2) -> bool:


    collision_sprite1 = SpriteCollision(sprite1)
    collision_sprite2 = SpriteCollision(sprite2)


    r1, r2 = collision_sprite1.get_rect(), collision_sprite2.get_rect()

    if r1.collides(r2):
        sprite2.color = (255, 255, 255)

        ri = r1.intersect(r2)
        x1_offset, y1_offset = int(ri.x1 - r1.x1), int(ri.y1 - r1.y1)
        x2_offset, y2_offset = int(ri.x1 - r2.x1), int(ri.y1 - r2.y1)
        d1, d2 = collision_sprite1.get_image(), collision_sprite2.get_image()
        p1 = memoryview(d1[0])
        p2 = memoryview(d2[0])
        for i in range(0, ri.width):
            for j in range(0, ri.height):
                c1 = p1[(x1_offset + i) + (j + y1_offset) * d1[1]]
                c2 = p2[(x2_offset + i) + (j + y2_offset) * d2[1]]
                if c1 > 0 and c2 > 0:
                    sprite2.color = (0, 255, 0)
                    return True

    else:
        sprite2.color = sprite2.default_color
    return False
