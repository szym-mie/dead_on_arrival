from typing import Any

from src.resource.loader import Loader


class TextLoader(Loader):
    def load(self) -> Any:
        return self.map_open('text', lambda p, f: f.read())
