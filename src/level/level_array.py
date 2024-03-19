from math import floor
from typing import Callable, TypeVar, Generic

from src.math.vector2 import Vector2

U = TypeVar('U')


class LevelArray(Generic[U]):
    x_size: int
    y_size: int

    def __init__(self, x_size: int, y_size: int, initial_factory: Callable[[], U]):
        self.x_size = x_size
        self.y_size = y_size

        self.a = [[initial_factory() for _ in range(y_size)] for _ in range(x_size)]

    def get_at(self, vec: Vector2) -> U:
        i = floor(vec.x)
        j = floor(vec.y)
        return self.a[i][j]

    def __index__(self, vec: Vector2) -> U:
        return self.get_at(vec)