from __future__ import annotations
from dataclasses import dataclass
from json import loads

from src.level.level_chunk import LevelChunk


@dataclass
class LevelImport:
    x_size: int
    y_size: int
    tile_ids: list[int]

    # TODO
    def chunkify(self) -> list[LevelChunk]:
        pass

    @staticmethod
    def from_json(json: str) -> LevelImport:
        obj = loads(json)
        return LevelImport(obj.x_size, obj.y_size, obj.data)

    @staticmethod
    def from_bitmap(x_size: int, y_size: int, pixel_colors: list[int]) -> LevelImport:
        def classify_colors(color: int) -> int:
            r = color & 0xff
            g = (color >> 8) & 0xff
            b = (color >> 16) & 0xff

            rc = 0 if r < 0x80 else 1
            gc = 0 if g < 0x80 else 2
            bc = 0 if b < 0x80 else 4

            return rc + gc + bc

        return LevelImport(x_size, y_size, [classify_colors(pc) for pc in pixel_colors])
