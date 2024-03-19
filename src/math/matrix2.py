from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

from src.math.vector2 import Vector2


@dataclass
class Matrix2:
    m: list[float] = field(default_factory=lambda: [0.0] * 4)

    @property
    def determinant(self) -> float:
        return self.m[0] * self.m[3] - self.m[1] * self.m[2]

    def _foreach(self, fn: Callable[[float], float]):
        self.m[0] = fn(self.m[0])
        self.m[1] = fn(self.m[1])
        self.m[2] = fn(self.m[2])
        self.m[3] = fn(self.m[3])

    def scale(self, scale: float) -> Matrix2:
        self._foreach(lambda n: n * scale)
        return self

    def invert(self) -> Matrix2:
        a = self.m[0]
        b = self.m[1]
        c = self.m[2]
        d = self.m[3]

        self.m[0] = d
        self.m[1] = -b
        self.m[2] = -c
        self.m[3] = a

        self.scale(1 / self.determinant)
        return self

    def multiply(self, mat: Matrix2) -> Matrix2:
        a = self.m[0]
        b = self.m[1]
        c = self.m[2]
        d = self.m[3]

        e = mat.m[0]
        f = mat.m[1]
        g = mat.m[2]
        h = mat.m[3]

        self.m[0] = a * e + b * g
        self.m[1] = a * f + b * h
        self.m[2] = c * e + d * g
        self.m[3] = c * f + d * h
        return self

    def apply(self, vec: Vector2) -> Vector2:
        a, b = vec.x, vec.y
        vec.x = self.m[0] * a + self.m[1] * b
        vec.y = self.m[2] * a + self.m[3] * b
        return vec

    def __mul__(self, other: Matrix2 | Vector2 | float) -> Matrix2 | Vector2:
        if isinstance(other, float):
            return self.scale(other)
        if isinstance(other, Matrix2):
            return self.multiply(other)
        if isinstance(other, Vector2):
            return self.apply(other)

    def __invert__(self) -> Matrix2:
        return self.scale(-1)

    def __len__(self):
        return 4

    def set(self, a: float, b: float, c: float, d: float) -> Matrix2:
        self.m[0] = a
        self.m[1] = b
        self.m[2] = c
        self.m[3] = d
        return self

    def set_from(self, mat: Matrix2) -> Matrix2:
        self.m[0] = mat.m[0]
        self.m[1] = mat.m[1]
        self.m[2] = mat.m[2]
        self.m[3] = mat.m[3]
        return self

    @property
    def as_tuple(self) -> (float, float, float, float):
        return tuple(self.m)

    @property
    def as_list(self) -> list[float]:
        return self.m

    def copy(self) -> Matrix2:
        return Matrix2().set_from(self)

    def __copy__(self) -> Matrix2:
        return self.copy()
