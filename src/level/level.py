from math import floor

from src.level.level_import import LevelImport


class Level:
    def __init__(self, level_import: LevelImport):
        self.chunk_size = 8
        self.chunks = level_import.chunkify(self.chunk_size)

    def draw(self, screen, x, y):
        for cx, cy, chunk in self.chunks.with_position():
            chunk.draw(screen, x + cx * chunk.size * 32, y + cy * chunk.size * 32)

    def resolve_chunk(self, x, y):
        return self.chunks.get_at(floor(x) // self.chunk_size,
                                  floor(y) // self.chunk_size)

    def get_tile_at(self, x, y):
        try:
            chunk = self.resolve_chunk(x, y)
            cx = floor(x) % self.chunk_size
            cy = floor(y) % self.chunk_size
            return chunk.tiles.get_at(cx, cy)
        except IndexError:
            return None

