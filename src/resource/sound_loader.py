from typing import Any

from pyglet import media

from src.resource.loader import Loader, register_loader


@register_loader('sound')
class SoundLoader(Loader):
    def load(self, resource_manager) -> Any:
        return self.map_open('binary', lambda p, f: media.load(p, file=f))
