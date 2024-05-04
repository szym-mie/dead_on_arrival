from typing import Any

from pyglet import image

from src.resource.loader import Loader


class ImageLoader(Loader):
    def load(self) -> Any:
        return self.map_open('binary', lambda p, f: image.load(p, file=f))
