from __future__ import annotations
from dataclasses import dataclass, field
from math import sqrt


@dataclass
class Vector2:
    """
    Float 2-component vector.
    """
    x: float = field(default=0.0)
    y: float = field(default=0.0)

    def add(self, vec: Vector2) -> Vector2:
        self.x += vec.x
        self.y += vec.y
        return self

    def sub(self, vec: Vector2) -> Vector2:
        self.x -= vec.x
        self.y -= vec.y
        return self

    def add_scalar(self, scalar: float) -> Vector2:
        self.x += scalar
        self.y += scalar
        return self

    def sub_scalar(self, scalar: float) -> Vector2:
        self.x -= scalar
        self.y -= scalar
        return self

    def multiply(self, vec: Vector2) -> Vector2:
        self.x *= vec.x
        self.y *= vec.y
        return self

    def scale(self, scale: float) -> Vector2:
        self.x *= scale
        self.y *= scale
        return self

    def __add__(self, other: Vector2 | float) -> Vector2:
        if isinstance(other, float):
            return self.add_scalar(other)
        if isinstance(other, Vector2):
            return self.add(other)

    def __sub__(self, other: Vector2 | float) -> Vector2:
        if isinstance(other, float):
            return self.sub_scalar(other)
        if isinstance(other, Vector2):
            return self.sub(other)

    def __mul__(self, other: Vector2 | float) -> Vector2:
        if isinstance(other, float):
            return self.scale(other)
        if isinstance(other, Vector2):
            return self.multiply(other)

    def __invert__(self) -> Vector2:
        return self.scale(-1)

    def __len__(self):
        return 2

    def set(self, x: float, y: float) -> Vector2:
        self.x = x
        self.y = y
        return self

    def set_from(self, vec: Vector2) -> Vector2:
        self.x = vec.x
        self.y = vec.y
        return self

    def normalize(self) -> Vector2:
        length = self.length
        if length != 0:
            self.scale(1 / length)
        return self

    def lerp(self, vec: Vector2, k: float) -> Vector2:
        self.x = self.x * (1 - k) + vec.x * k
        self.y = self.y * (1 - k) + vec.y * k
        return self

    @property
    def length(self) -> float:
        return sqrt(self.length_sqr)

    @property
    def length_sqr(self) -> float:
        return self.x ** 2 + self.y ** 2

    def dist_to(self, vec: Vector2) -> float:
        return self.copy().sub(vec).length

    def abs(self) -> Vector2:
        self.x = abs(self.x)
        self.y = abs(self.y)
        return self

    def min_component(self) -> float:
        return min(self.x, self.y)

    def max_component(self) -> float:
        return max(self.x, self.y)

    @property
    def as_tuple(self) -> (float, float):
        return self.x, self.y

    @property
    def as_list(self) -> list[float]:
        return [self.x, self.y]

    def copy(self) -> Vector2:
        return Vector2().set_from(self)

    def __copy__(self) -> Vector2:
        return self.copy()
