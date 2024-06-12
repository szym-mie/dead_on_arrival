from pyglet.math import Vec2

from src.util.unit import Unit


class World(Unit):
    def __init__(self):
        self.level = None

        # FIXME: lol
        self.entities = []

    def spawn(self, entity, x, y, rotation):
        entity.position.x = x
        entity.position.y = y
        entity.rotation = rotation
        self.entities.append(entity)

    def remove(self, entity):
        self.entities.remove(entity)

    def update(self, delta_time, characters):
        for entity in self.entities:
            last_x = entity.position.x
            last_y = entity.position.y
            entity.update(delta_time)
            x = entity.position.x
            y = entity.position.y

            pos0 = Vec2(x, y)
            pos1 = Vec2(*World.lerp(x, y, last_x, last_y, .25))
            pos2 = Vec2(*World.lerp(x, y, last_x, last_y, .50))
            pos3 = Vec2(*World.lerp(x, y, last_x, last_y, .75))

            for i in range(len(characters)):
                try:
                    rect, char, bcircle = characters[i]
                    if (bcircle.test_point(pos0) or bcircle.test_point(pos1) or
                            bcircle.test_point(pos2) or bcircle.test_point(pos3)):
                        print(entity.base_damage)
                        char.deal_damage(entity.base_damage)
                        entity.rect.remove()
                        self.remove(entity)
                        if char.is_dead:
                            rect.remove()
                            del characters[i]
                        print('hit: ', char)
                except IndexError:
                    pass

            tile0 = self.level.get_tile_at(*pos0)
            tile1 = self.level.get_tile_at(*pos1)
            tile2 = self.level.get_tile_at(*pos2)
            tile3 = self.level.get_tile_at(*pos3)

            if tile0 is None or tile1 is None or tile2 is None or tile3 is None:
                entity.rect.remove()
                self.remove(entity)
                continue
            if (World.can_collide_projectile(tile0) or
                    World.can_collide_projectile(tile1) or
                    World.can_collide_projectile(tile2) or
                    World.can_collide_projectile(tile3)):
                entity.rect.remove()
                self.remove(entity)

    @staticmethod
    def can_collide_projectile(tile):
        return tile.is_solid and not tile.is_slab

    @staticmethod
    def can_collide_entity(tile):
        return tile.is_solid

    @staticmethod
    def lerp(x1, y1, x2, y2, q):
        qi = 1 - q
        return x1 * q + x2 * qi, y1 * q + y2 * qi


world = World.default()
