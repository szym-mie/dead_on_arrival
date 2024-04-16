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

    def chunkify(self, size) -> LevelArray[LevelChunk]:
        x_chunks = ceil(self.x_size / size)
        y_chunks = ceil(self.y_size / size)

        chunk_array = LevelArray(x_chunks, y_chunks, lambda: LevelChunk(size))

        for x, y, new_chunk in chunk_array.with_position():
            new_chunk.populate_chunk(x * size, y * size, self.y_size, self.tile_ids)
            new_chunk.update_layers()

        return chunk_array

    @staticmethod
    def from_json(json: str) -> LevelImport:
        obj = loads(json)
        # return LevelImport(obj['x_size'], obj['y_size'], obj['tile'], obj['entity'])
        return LevelImport(obj['x_size'], obj['y_size'], obj['tile'], [])

    @staticmethod
    def from_bitmap(x_size: int, y_size: int, tile_colors: list[int], entity_colors: list[int]) -> LevelImport:
        def classify_colors(color: int) -> int:
            r = color & 0xff
            g = (color >> 8) & 0xff
            b = (color >> 16) & 0xff

            rc = r // 0x40
            gc = g // 0x40
            bc = b // 0x40

            return rc + gc + bc

        return LevelImport(x_size, y_size,
                           [classify_colors(tc) for tc in tile_colors],
                           [classify_colors(ec) for ec in entity_colors])
