from src.level.level_array import LevelArray


class LevelChunk:
    tiles = LevelArray(8, 8, lambda: 0)
    entities = []

