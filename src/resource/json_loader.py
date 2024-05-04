import json
from typing import Any

from src.resource.loader import Loader


class JSONLoader(Loader):
    def load(self) -> Any:
        return self.map_open('text', lambda p, f: json.load(f))
