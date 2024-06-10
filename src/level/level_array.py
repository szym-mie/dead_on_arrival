from typing import Callable, TypeVar, Generic

U = TypeVar('U')


class LevelArray(Generic[U]):
    x_size: int
    y_size: int

    def __init__(self, x_size: int, y_size: int, initial_factory: Callable[[], U]):
        self.x_size = x_size
        self.y_size = y_size

        self.array = [[initial_factory() for _ in range(y_size)] for _ in range(x_size)]

    def get_at(self, i: int, j: int) -> U:
        return self.array[i][j]

    def put_at(self, i: int, j: int, u: U) -> None:
        self.array[i][j] = u

    def with_position(self):
        for x in range(self.x_size):
            for y in range(self.y_size):
                yield x, y, self.array[x][y]

    def map(self, func):
        new_array = LevelArray(self.x_size, self.y_size, lambda: None)

        for x in range(self.x_size):
            for y in range(self.y_size):
                new_array.put_at(x, y, func(self, x, y))

        return new_array
