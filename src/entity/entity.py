from abc import abstractmethod, ABC


class Entity(ABC):
    def __init__(self, position):
        self.position = position
        self.time = 0

    @abstractmethod
    def update(self, delta_time):
        self.time += delta_time
