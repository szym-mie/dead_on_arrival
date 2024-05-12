from src.level.level import Level
from src.util.unit import Unit


class World(Unit):
    def __init__(self):
        self.level = Level.empty()

    def spawn(self, entity, x, y):
        pass

    def update(self, delta_time):
        pass


world = World.default()
