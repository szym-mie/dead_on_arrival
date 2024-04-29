from __future__ import annotations
from dataclasses import dataclass, field
from math import sqrt

from pyglet.math import Vec2

from src.math.bbox import BBox
from src.math.btester import BTester


@dataclass
class BCircle(BTester):
    center: Vec2 = field(default_factory=lambda: Vec2())
    radius: float = field(default=0.0)

    @property
    def size(self):
        return self.radius * 2

    def test_point(self, vec: Vec2) -> bool:
        return self.center.dist_to(vec) <= self.radius

    def test_line(self, vec_a: Vec2, vec_b: Vec2) -> bool:
        return False

    def test_bcircle(self, other: BCircle) -> bool:
        return self.center.distance(other.center) <= self.radius + other.radius

    def test_bbox(self, box: BBox) -> bool:
        circle_dist = box.center - self.center
        circle_dist_abs = Vec2(abs(circle_dist.x), abs(circle_dist.y))
        half_size = box.size * 0.5
        corner_dist = circle_dist_abs.distance(half_size)

        if circle_dist.x <= half_size.x or circle_dist.y <= half_size.y:
            return True

        half_size += Vec2(self.radius, self.radius)
        if circle_dist.x > half_size.x or circle_dist.y > half_size.y:
            return False

        return corner_dist <= self.radius ** 2

    @staticmethod
    def from_bbox_contain(bbox: BBox) -> BCircle:
        center = bbox.center
        radius = min(bbox.size.x, bbox.size.y) / 2

        return BCircle(center, radius)

    @staticmethod
    def from_bbox_diagonal(bbox: BBox) -> BCircle:
        center = bbox.center
        radius = bbox.size.length / 2

        return BCircle(center, radius)
