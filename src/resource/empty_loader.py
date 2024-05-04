from typing import Any

from src.resource.loader import Loader


class EmptyLoader(Loader):
    def load(self) -> Any:
        return None
