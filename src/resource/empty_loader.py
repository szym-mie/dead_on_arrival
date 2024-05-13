from typing import Any

from src.resource.loader import Loader, register_loader


@register_loader('empty')
class EmptyLoader(Loader):
    def load(self, resource_manager) -> Any:
        return None
