from __future__ import annotations

from pyglet.math import Vec2

from src.bounds.btester import BTester


class BBox(BTester):
    def __init__(self, lower_corner, size):
        self.lower = lower_corner
        self.upper = lower_corner + size
        self.size = size

    @property
    def center(self) -> Vec2:
        return (self.size * 0.5) + self.lower

    def test_point(self, vec):
        # TODO return vector or none
        upper = self.upper
        return \
            self.lower.x <= vec.x <= upper.x and \
            self.lower.y <= vec.y <= upper.y

    def test_bray(self, other):
        # TODO return vector or none
        pass

    def test_bbox(self, other):
        # TODO return vector or none
        xa, ya = self.lower
        wa, ha = self.size
        xb, yb = other.lower
        wb, hb = other.size
        return \
            xa < xb + wb and xa + wa > xb and \
            ya < yb + hb and ya + ha > yb

    def test_bcircle(self, other):
        # TODO return vector or none
        return other.test_bbox(self)

    @staticmethod
    def from_points(lower: Vec2, upper: Vec2) -> BBox:
        return BBox(lower, upper - lower)

    @staticmethod
    def from_center(center: Vec2, size: Vec2) -> BBox:
        half_size = size * 0.5
        return BBox(center - half_size, size)
