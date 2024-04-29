from pyglet import image
from pyglet.sprite import Sprite

from src.level.level_array import LevelArray


class LevelChunk:
    def __init__(self, size):
        self.size = size
        self.tiles = LevelArray(size, size, lambda: 0)
        self.entities = []
        self.layers = []

    def put_tile_at(self, i, j, tile):
        self.tiles.put_at(i % self.size, j % self.size, tile)

    def put_entity_at(self, entity):
        self.entities.append(entity)

    def populate_chunk(self, start_x, start_y, size_x, tile_ids):
        for ty in range(start_y, start_y + self.size):
            for tx in range(start_x, start_x + self.size):
                i = ty * size_x + tx
                self.put_tile_at(tx, ty, tile_ids[i])

    def update_layers(self, wall_image, floor_image):
        layer_texture = image.create(32 * self.size, 32 * self.size).get_texture()
        main_layer = Sprite(layer_texture)
        self.layers = [main_layer]

        def get_tile_surface(tile_id):
            if tile_id == 0:
                return wall_image
            else:
                return floor_image

        for x, y, tid in self.tiles.with_position():
            main_layer.image.blit_into(get_tile_surface(tid), x * 32, y * 32, 0)

    def draw(self, x, y):
        for layer in self.layers:
            layer.update(x, y, 0.0, 0, 2.0)
            layer.draw()
