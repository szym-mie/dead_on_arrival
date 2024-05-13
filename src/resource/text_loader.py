from typing import Any

from src.resource.loader import Loader, register_loader


@register_loader('text')
class TextLoader(Loader):
    def load(self, resource_manager) -> Any:
        return self.map_open('text', lambda p, f: f.read())
