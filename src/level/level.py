from math import floor, ceil

from src.level.level_import import LevelImport


class Level:
    def __init__(self, level_import: LevelImport):
        self.chunk_size = 8
        self.chunks = level_import.chunkify(self.chunk_size)

    def draw(self, x, y):
        for cx, cy, chunk in self.chunks.with_position():
            chunk.draw(x + cx * chunk.size * 64, y + cy * chunk.size * 64)

    def resolve_chunk(self, x, y):
        return self.chunks.get_at(floor(x) // self.chunk_size,
                                  floor(y) // self.chunk_size)

    def test_collisions(self, line_start, line_end):
        chunk = self.resolve_chunk(line_start.x, line_start.y)

        dir_x = line_end.x - line_start.x
        dir_y = line_end.y - line_start.y

        tan_x = dir_y / dir_x
        tan_y = dir_x / dir_y

        print(tan_x)
        print(tan_y)

        mod_x = line_start.x % 1.0
        mod_y = line_start.y % 1.0
        dx = 1.0 - mod_x if dir_x > 0 else mod_x
        dy = 1.0 - mod_y if dir_y > 0 else mod_y

        print(dx * tan_x)
        print(dy * tan_y)
        step_x = line_start.x + dy * tan_y
        real_y = ceil(line_start.y) if dir_x > 0 else floor(line_start.y)
        step_y = line_start.y + dx * tan_x
        real_x = ceil(line_start.x) if dir_y > 0 else floor(line_start.x)

        while True:
            break

        print(step_x)
        print(step_y)

    def get_chunks_on_line(self, line_start, line_end):
        chunk_start = self.resolve_chunk(line_start.x, line_start.y)
        chunk_end = self.resolve_chunk(line_end.x, line_end.y)

    def get_tile_at(self, x, y):
        try:
            chunk = self.resolve_chunk(x, y)
            cx = floor(x) % self.chunk_size
            cy = floor(y) % self.chunk_size
            return chunk.tiles.get_at(cx, cy)
        except IndexError:
            return None

    def all_tiles(self):
        for cx, cy, chunk in self.chunks.with_position():
            for x, y, tile in chunk.tiles.with_position():
                yield cx * chunk.size + x, cy * chunk.size + y, tile

    @classmethod
    def empty(cls):
        return cls(LevelImport.empty())
