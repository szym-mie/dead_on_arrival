from typing import Any

from pyglet import image

from src.resource.loader import Loader, register_loader


@register_loader('image')
class ImageLoader(Loader):
    def load(self, resource_manager) -> Any:
        return self.map_open('binary', lambda p, f: image.load(p, file=f))
