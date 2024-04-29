import json
from typing import Any

from src.resource.loader import Loader


class JSONLoader(Loader):
    def load(self) -> Any:
        return Loader.map_open(self.url,
                               Loader.FileType.text,
                               lambda f: json.load(f))
