from abc import ABC, abstractmethod


class Loader(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def load(self, resource_manager):
        return NotImplemented

    def map_open(self, file_type: str, map_fn):
        if file_type == 'text':
            mode = 'r'
            with open(self.url, mode, encoding='utf-8') as file:
                return map_fn(self.url, file)
        elif file_type == 'binary':
            mode = 'rb'
            with open(self.url, mode) as file:
                return map_fn(self.url, file)


registered_loaders = {}


def register_loader(loader_id):
    def _register_decorator(cls):
        registered_loaders[loader_id] = cls
        return cls
    return _register_decorator
