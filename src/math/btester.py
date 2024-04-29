from __future__ import annotations

from abc import abstractmethod, ABC

from pyglet.math import Vec2

from src.math.bbox import BBox
from src.math.bcircle import BCircle


class BTester(ABC):
    @abstractmethod
    def test_point(self, vec: Vec2) -> bool:
        pass

    @abstractmethod
    def test_line(self, vec_a: Vec2, vec_b: Vec2) -> bool:
        pass

    @abstractmethod
    def test_bbox(self, other: BBox) -> bool:
        pass

    @abstractmethod
    def test_bcircle(self, other: BCircle) -> bool:
        pass
