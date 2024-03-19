from __future__ import annotations
from dataclasses import dataclass, field

from src.math.bbox import BBox
from src.math.btester import BTester
from src.math.vector2 import Vector2


@dataclass
class BCircle(BTester):
    center: Vector2 = field(default_factory=lambda: Vector2())
    radius: float = field(default=0.0)

    @property
    def size(self):
        return self.radius * 2

    def test_point(self, vec: Vector2) -> bool:
        return self.center.dist_to(vec) <= self.radius

    def test_bcircle(self, other: BCircle) -> bool:
        return self.center.dist_to(other.center) <= self.radius + other.radius

    def test_bbox(self, box: BBox) -> bool:
        circle_dist = box.center.copy().sub(self.center).abs()
        half_size = box.size.copy().scale(0.5)
        corner_dist = circle_dist.dist_to(half_size)

        if circle_dist.x <= half_size.x or circle_dist.y <= half_size.y:
            return True

        half_size.add_scalar(self.radius)
        if circle_dist.x > half_size.x or circle_dist.y > half_size.y:
            return False

        return corner_dist <= self.radius ** 2

    @staticmethod
    def from_bbox_contain(bbox: BBox) -> BCircle:
        center = bbox.center
        radius = bbox.size.min_component() / 2

        return BCircle(center, radius)

    @staticmethod
    def from_bbox_diagonal(bbox: BBox) -> BCircle:
        center = bbox.center
        radius = bbox.size.length / 2

        return BCircle(center, radius)
