import json
from typing import Any

from src.resource.loader import Loader, register_loader


@register_loader('json')
class JSONLoader(Loader):
    def load(self, resource_manager) -> Any:
        return self.map_open('text', lambda p, f: json.load(f))
