from dataclasses import dataclass
from math import sqrt

from pyglet.math import Vec2

from src.math.bbox import BBox
from src.math.bcircle import BCircle
from src.math.btester import BTester


class BLine(BTester):
    def __init__(self, vec_a: Vec2, vec_b: Vec2):
        self.vec_a = vec_a
        self.vec_b = vec_b
        dy = self.vec_b.y - self.vec_a.y
        dx = self.vec_a.x - self.vec_b.x
        self.a = dy
        self.b = dx
        self.c = self.vec_a.y * dx + self.vec_a.x * dy

    def _distance_to_point(self, vec: Vec2) -> float:
        p = abs(self.a * vec.x + self.b * vec.y + self.c)
        m = sqrt(self.a * self.a + self.b * self.b)
        return p / m

    def test_point(self, vec: Vec2) -> bool:
        e = 0.00001
        return self._distance_to_point(vec) < e

    def test_line(self, vec_a: Vec2, vec_b: Vec2) -> bool:
        return False

    def test_bbox(self, other: BBox) -> bool:
        return False

    def test_bcircle(self, other: BCircle) -> bool:
        pass
        # TODO
        # ld = vec_b.distance(vec_a)
        #
        # d =
        # if d < self.radius:
        #     cad = self.center.distance(vec_a)
        #     cbd = self.center.distance(vec_b)
        #     return True
