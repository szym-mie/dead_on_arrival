from typing import Any

from pyglet import media

from src.resource.loader import Loader


class SoundLoader(Loader):
    def load(self) -> Any:
        return self.map_open('binary', lambda p, f: media.load(p, file=f))
