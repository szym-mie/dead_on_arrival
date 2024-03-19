from __future__ import annotations
from abc import abstractmethod, ABC

from src.math.bbox import BBox
from src.math.bcircle import BCircle
from src.math.vector2 import Vector2


class BTester(ABC):
    @abstractmethod
    def test_point(self, vec: Vector2) -> bool:
        pass

    @abstractmethod
    def test_bbox(self, other: BBox) -> bool:
        pass

    @abstractmethod
    def test_bcircle(self, other: BCircle) -> bool:
        pass
