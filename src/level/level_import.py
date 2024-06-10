from __future__ import annotations

from dataclasses import dataclass
from json import loads
from math import ceil

from src.level.level_array import LevelArray
from src.level.level_chunk import LevelChunk
from src.level.level_tile import LevelTile


@dataclass
class LevelImport:
    x_size: int
    y_size: int
    tiles: list[LevelTile]

    def chunkify(self, chunk_size) -> LevelArray[LevelChunk]:
        x_chunks = ceil(self.x_size / chunk_size)
        y_chunks = ceil(self.y_size / chunk_size)

        chunk_array = LevelArray(x_chunks, y_chunks, lambda: LevelChunk(chunk_size))

        for x, y, new_chunk in chunk_array.with_position():
            new_chunk.populate_chunk(x * chunk_size, y * chunk_size, self.x_size, self.tiles)

        return chunk_array

    @classmethod
    def empty(cls) -> LevelImport:
        return cls(0, 0, [])

    @classmethod
    def from_json(cls, json: str) -> LevelImport:
        obj = loads(json)

        x_size = obj['x_size']
        y_size = obj['y_size']
        wall_ids = obj['walls']
        spawn_ids = obj['spawns']

        return LevelImport._create_tiles_from_ids(x_size, y_size, wall_ids, spawn_ids)

    @classmethod
    def from_bitmap(cls, x_size: int, y_size: int, wall_colors: list[int], spawn_colors: list[int]) -> LevelImport:
        def classify_colors(r, g, b) -> int:
            rc = r // 0x40
            gc = g // 0x40
            bc = b // 0x40

            return rc * 16 + gc * 4 + bc

        def color_iter(components) -> (int, int, int):
            return list(zip(*[iter(components)] * 3))

        wall_ids = [classify_colors(*tc) for tc in color_iter(wall_colors)]
        spawn_ids = [classify_colors(*ec) for ec in color_iter(spawn_colors)]

        return LevelImport._create_tiles_from_ids(x_size, y_size, wall_ids, spawn_ids)

    @classmethod
    def from_images(cls, wall_img, spawn_img) -> LevelImport:
        wall_img_data = wall_img.get_image_data()
        spawn_img_data = spawn_img.get_image_data()

        if (
                wall_img_data.width != spawn_img_data.width and
                wall_img_data.height != spawn_img_data.height):
            raise RuntimeError('images with unequal dimensions')

        x_size = wall_img_data.width
        y_size = wall_img_data.height

        level_img_fmt = 'RGB'
        level_img_pitch = x_size * len(level_img_fmt)
        wall_pix = list(wall_img_data.get_data(level_img_fmt, level_img_pitch))
        spawn_pix = list(spawn_img_data.get_data(level_img_fmt, level_img_pitch))

        return cls.from_bitmap(x_size, y_size, wall_pix, spawn_pix)

    @classmethod
    def _create_tiles_from_ids(cls, x_size, y_size, wall_ids, spawn_ids):
        def wall_is_solid(wall_id):
            return wall_id >= 16

        def wall_is_slab(wall_id):
            return 16 <= wall_id < 32

        def wall_z(wall_id):
            if wall_id < 16:
                return 0.0
            elif wall_id < 32:
                return 0.5
            elif wall_id < 48:
                return 1.0
            elif wall_id < 60:
                return 2.0
            else:
                return 4.0

        tiles = [
            LevelTile.create_with_default_suppliers(
                wall_id,
                spawn_id,
                wall_is_solid,
                wall_is_slab,
                wall_z
            ) for wall_id, spawn_id in zip(wall_ids, spawn_ids)
        ]

        return cls(x_size, y_size, tiles)
