from __future__ import annotations

from abc import abstractmethod, ABC


class BTester(ABC):
    @abstractmethod
    def test_point(self, vec):
        pass

    @abstractmethod
    def test_bray(self, other):
        pass

    @abstractmethod
    def test_bbox(self, other):
        pass

    @abstractmethod
    def test_bcircle(self, other):
        pass
