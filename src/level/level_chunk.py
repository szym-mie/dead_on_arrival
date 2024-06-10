from src.level.level_array import LevelArray


class LevelChunk:
    def __init__(self, size):
        self.size = size
        self.tiles = LevelArray(size, size, lambda: None)
        self.entities = []
        self.layers = []

    def put_tile_at(self, i, j, tile):
        self.tiles.put_at(i % self.size, j % self.size, tile)

    def put_entity_at(self, entity):
        self.entities.append(entity)

    def populate_chunk(self, start_x, start_y, size_x, tiles):
        for ty in range(start_y, start_y + self.size):
            for tx in range(start_x, start_x + self.size):
                i = ty * size_x + tx
                self.put_tile_at(tx, ty, tiles[i])

    def draw(self, x, y):
        for layer in self.layers:
            layer.update(x, y, 0.0, 0, 2.0)
            layer.draw()
