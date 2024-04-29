from src.level.level import Level
from src.util.unit import Unit


class World(Unit):
    def __init__(self):
        self.level = Level.empty()

    def spawn(self, entity, x, y):

