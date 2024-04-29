from __future__ import annotations

from abc import abstractmethod, ABC

from pyglet.math import Vec2


class BTester(ABC):
    @abstractmethod
    def test_point(self, vec: Vec2) -> bool:
        pass

    @abstractmethod
    def test_bray(self, other) -> bool:
        pass

    @abstractmethod
    def test_bbox(self, other) -> bool:
        pass

    @abstractmethod
    def test_bcircle(self, other) -> bool:
        pass
