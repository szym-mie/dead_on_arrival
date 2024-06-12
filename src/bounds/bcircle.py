from __future__ import annotations
from math import sqrt

from pyglet.math import Vec2

from src.bounds.btester import BTester


class BCircle(BTester):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def size(self):
        return self.radius * 2

    def test_point(self, vec):
        # TODO return vector or none
        return self.center.distance(vec) <= self.radius

    def test_bray(self, other):
        # TODO return vector or none
        return False

    def test_bbox(self, other):
        # TODO return vector or none
        circle_dist = other.center - self.center
        circle_dist_abs = Vec2(abs(circle_dist.x), abs(circle_dist.y))
        half_size = other.size * 0.5
        corner_dist = circle_dist_abs.distance(half_size)

        if circle_dist.x <= half_size.x or circle_dist.y <= half_size.y:
            return True

        half_size += Vec2(self.radius, self.radius)
        if circle_dist.x > half_size.x or circle_dist.y > half_size.y:
            return False

        return corner_dist <= self.radius ** 2

    def test_bcircle(self, other):
        # TODO return vector or none
        return self.center.distance(other.center) <= self.radius + other.radius

    @staticmethod
    def from_bbox_contain(bbox) -> BCircle:
        center = bbox.center
        radius = min(bbox.size.x, bbox.size.y) / 2

        return BCircle(center, radius)

    @staticmethod
    def from_bbox_diagonal(bbox) -> BCircle:
        center = bbox.center
        radius = bbox.size.length / 2

        return BCircle(center, radius)
