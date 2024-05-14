from src.util.unit import Unit


class World(Unit):
    def __init__(self):
        self.level = None

        # FIXME: lol
        self.entities = []

    def spawn(self, entity, x, y):
        entity.position.x = x
        entity.position.y = y
        self.entities.append(entity)

    def remove(self, entity):
        self.entities.remove(entity)

    def update(self, delta_time):
        for entity in self.entities:
            last_x = entity.position.x
            last_y = entity.position.y
            entity.update(delta_time)
            x = entity.position.x
            y = entity.position.y
            if (self.level.get_tile_at(x, y) == 0 or
                    self.level.get_tile_at(*World.lerp(x, y, last_x, last_y, .5)) == 0 or
                    self.level.get_tile_at(*World.lerp(x, y, last_x, last_y, .25)) == 0 or
                    self.level.get_tile_at(*World.lerp(x, y, last_x, last_y, .75)) == 0):
                self.remove(entity)

    @staticmethod
    def lerp(x1, y1, x2, y2, q):
        qi = 1 - q
        return x1 * q + x2 * qi, y1 * q + y2 * qi


world = World.default()
