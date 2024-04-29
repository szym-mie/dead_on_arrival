from __future__ import annotations
from dataclasses import dataclass, field

from pyglet.math import Vec2

from src.math.bcircle import BCircle
from src.math.btester import BTester


@dataclass
class BBox(BTester):
    lower: Vec2 = field(default_factory=lambda: Vec2())
    size: Vec2 = field(default_factory=lambda: Vec2())

    @property
    def upper(self) -> Vec2:
        return self.lower.copy().add(self.size)

    @property
    def center(self) -> Vec2:
        return self.size.copy().scale(0.5).add(self.lower)

    def test_point(self, vec: Vec2) -> bool:
        upper = self.upper
        return \
            self.lower.x <= vec.x <= upper.x and \
            self.lower.y <= vec.y <= upper.y

    def test_bbox(self, other: BBox) -> bool:
        xa, ya = self.lower
        wa, ha = self.size
        xb, yb = other.lower
        wb, hb = other.size
        return \
            xa < xb + wb and xa + wa > xb and \
            ya < yb + hb and ya + ha > yb

    def test_bcircle(self, circle: BCircle) -> bool:
        return circle.test_bbox(self)

    @staticmethod
    def from_points(lower: Vec2, upper: Vec2) -> BBox:
        return BBox(lower.copy(), upper.copy().sub(lower))

    @staticmethod
    def from_center(center: Vec2, size: Vec2) -> BBox:
        half_size = size.copy().abs().scale(0.5)
        return BBox(center.copy().sub(half_size), size.copy())
