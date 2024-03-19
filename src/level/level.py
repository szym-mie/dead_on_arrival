from src.level.level_import import LevelImport


class Level:
    def __init__(self, level_import: LevelImport):
        self.chunks = level_import.chunkfiy()



