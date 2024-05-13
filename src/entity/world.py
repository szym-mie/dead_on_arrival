from src.util.unit import Unit


class World(Unit):
    def __init__(self, level):
        self.level = level

    def spawn(self, entity, x, y):
        pass

    def update(self, delta_time):
        pass


world = World.default()
