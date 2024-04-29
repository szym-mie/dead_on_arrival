from __future__ import annotations

from dataclasses import dataclass
from json import loads
from math import ceil

from src.level.level_array import LevelArray
from src.level.level_chunk import LevelChunk


@dataclass
class LevelImport:
    x_size: int
    y_size: int
    tile_ids: list[int]
    entity_ids: list[int]

    def chunkify(self, wall_image, floor_image, chunk_size) -> LevelArray[LevelChunk]:
        x_chunks = ceil(self.x_size / chunk_size)
        y_chunks = ceil(self.y_size / chunk_size)

        chunk_array = LevelArray(x_chunks, y_chunks, lambda: LevelChunk(chunk_size))

        for x, y, new_chunk in chunk_array.with_position():
            new_chunk.populate_chunk(x * chunk_size, y * chunk_size, self.y_size, self.tile_ids)
            new_chunk.update_layers(wall_image, floor_image)

        return chunk_array

    @classmethod
    def empty(cls) -> LevelImport:
        return cls(0, 0, [], [])

    @classmethod
    def from_json(cls, json: str) -> LevelImport:
        obj = loads(json)
        return cls(obj['x_size'], obj['y_size'], obj['tile'], [])

    @classmethod
    def from_bitmap(cls, x_size: int, y_size: int, tile_colors: list[int], entity_colors: list[int]) -> LevelImport:
        def classify_colors(r, g, b) -> int:
            rc = r // 0x40
            gc = g // 0x40
            bc = b // 0x40

            return rc + gc + bc

        def color_iter(components) -> (int, int, int):
            return list(zip(*[iter(components)] * 3))

        return cls(x_size, y_size,
                   [classify_colors(*tc) for tc in color_iter(tile_colors)],
                   [classify_colors(*ec) for ec in color_iter(entity_colors)])
